import subprocess
import requests
import pytz, calendar, time, threading, json
from datetime import datetime

class WXBot(object):

    def __init__(self, verbose=False):
        # Predefine request strings
        self._hrefLoginFormat = 'https://wx.qq.com/jslogin?appid=wx782c26e4c19acffb&redirect_uri=https%3A%2F%2Fwx.qq.com%2Fcgi-bin%2Fmmwebwx-bin%2Fwebwxnewloginpage&fun=new&lang=en_GB&_={}'

        self._hrefQRCodeFormat = 'https://login.weixin.qq.com/qrcode/{}'

        self._herfScanFormat = 'https://login.weixin.qq.com/cgi-bin/mmwebwx-bin/login?loginicon=true&uuid={}&tip=0&r={}&_={}'

        self._herfWXInit = 'https://wx.qq.com/cgi-bin/mmwebwx-bin/webwxinit?r={}&lang=en_GB&pass_ticket={}'

        self._hrefWXGetContacts = 'https://wx.qq.com/cgi-bin/mmwebwx-bin/webwxgetcontact?lang=en_GB&pass_ticket={}&r={}&skey={}'

        self._hrefSynccheck =  'https://webpush.wx.qq.com/cgi-bin/mmwebwx-bin/synccheck?r={}&skey={}&sid={}&uin={}&deviceid={}&synckey={}&_={}'

        self._hrefWebwxsync = 'https://wx.qq.com/cgi-bin/mmwebwx-bin/webwxsync?sid={}&skey={}&lang=en_GB&pass_ticket={}'

        self._hrefSendMessage = 'https://wx.qq.com/cgi-bin/mmwebwx-bin/webwxsendmsg?lang=en_GB&pass_ticket={}'

        # Header Settings
        self.headers = {
            'Pragma': 'no-cache',
            'Origin': 'https://wx.qq.com',
            'Accept-Language': 'en-GB,en-US;q=0.8,en;q=0.6,it;q=0.4,zh-CN;q=0.2,zh-TW;q=0.2',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/45.0.2454.85 Chrome/45.0.2454.85 Safari/537.36',
            'Content-Type': 'application/json;charset=UTF-8',
            'Accept': 'application/json, text/plain, */*',
            'Cache-Control': 'no-cache',
            'Referer': 'https://wx.qq.com/?&lang=en_GB'
        }

        # global variables
        self.isLoggedIn = False
        self.isRunning = False
        self.status = 0
        self.avatar = ""
        self.uuid = ""
        self.skey = ""
        self.wxsid = ""
        self.wxuin = ""
        self.deviceID = 'e690869071029209'
        self.pass_ticket = ""
        self.contacts = []
        self.synckey = []
        self.init_info = {}
        self._verbose = verbose
        self._listeners = {}
        # Session Management
        self.session = requests.Session()
        self.session.headers.update(self.headers)

    # helper functions
    def _get_unix_timestamp(self, time_zone='UTC'):
        dt = datetime.now()
        tz = pytz.timezone(time_zone)
        utc_dt = tz.localize(dt, is_dst=True).astimezone(pytz.utc)
        return calendar.timegm(utc_dt.timetuple())

    def _find_between(self, s, first, last ):
        try:
            start = s.index( first ) + len( first )
            end = s.index( last, start )
            return s[start:end]
        except ValueError:
            return ""

    def _fire_event(self, event, args):
        if event in self._listeners:
            for func in self._listeners[event]:
                func(args)

    # request hendler
    def _request_get_contacts(self):
        response = wxGet(self.session, self._hrefWXGetContacts.format(
            self.pass_ticket,
            self._get_unix_timestamp(),
            self.skey
        ))

        data = response.json()
        if data['BaseResponse']['Ret'] == 0:
            self.contacts = data['MemberList']
        else:
            print ('Failed to get contacts list.')

    def _request_synccheck(self):

        def format_synckey():
            return '%7C'.join(
                ['{}_{}'.format(k['Key'], k['Val']) for k in self.synckey]
            )

        str_request =  self._hrefSynccheck.format(
            self._get_unix_timestamp(),
            self.skey,
            self.wxsid,
            self.wxuin,
            self.deviceID,
            format_synckey(),
            self._get_unix_timestamp()
        )

        response = wxGet(self.session, str_request)

        retcode = int(self._find_between(response.text,'retcode:"','"'))
        selector = int(self._find_between(response.text,'selector:"','"}'))

        print ('Sync Check Done:')
        print (response.text)

        if not retcode == 0:
            self.isLoggedIn = False
            self.status = 0
            return

        if selector == 0:
            print ('Status Idel')
        else:
            # Get New Messages
            if selector == 6:
                self._request_get_update()

    def _request_get_update(self):
        # Send request for update
        data = {
            "BaseRequest":{
                "Uin": self.wxuin,
                "Sid": self.wxsid,
                "Skey": self.skey,
                "DeviceID": self.deviceID
            },"SyncKey":{
                "Count":len(self.synckey),
                "List":self.synckey
            },"rr":self._get_unix_timestamp()
        }

        response = wxPost(self.session, self._hrefWebwxsync.format(
            self.wxsid,
            self.skey,
            self.pass_ticket
        ), data=data)

        if self._verbose:
            print ('Message Recieved:')

        data = response.json()
        self.synckey = data['SyncKey']['List']

        # parse data
        msglist = data['AddMsgList']
        for msg in msglist:
            if self._verbose:
                print ('({}){}-{}:{}'.format(
                    msg['MsgType'],
                    msg['FromUserName'],
                    msg['ToUserName'],
                    msg['Content'].encode('raw_unicode_escape').decode('utf8')
                ))

            # fire event
            # if msg['MsgType'] == 1:
            self._fire_event('onmessage', msg)

    def _request_login(self):
        while(not self.isLoggedIn):

            response = wxGet(self.session, self._hrefLoginFormat.format(self._get_unix_timestamp()))

            self.uuid = self._find_between(response.text,'uuid = \"',"\";")
            self.hrefQR = self._hrefQRCodeFormat.format(self.uuid)

            print (self.hrefQR)
            # wait for scan
            while(not self.isLoggedIn):
                response = wxGet(self.session, self._herfScanFormat.format(
                    self.uuid, self._get_unix_timestamp(),self._get_unix_timestamp()
                ))

                if not response:
                    break

                line = response.text
                code = self._find_between(line, 'window.code=', ';')
                if code == "408":
                    self.status = 0
                    print ("Please Scan QR Code")
                elif code == '201':
                    self.status = 1
                    self.avatar = self._find_between(line.replace(' ',''), "window.userAvatar='", "';")
                    print ("Please accept login on your phone")
                elif code == '200':
                    self.status = 2
                    print ('Initialising...')

                    urlredirect = self._find_between(
                        line,
                        'window.redirect_uri="',
                        '";'
                    ) + '&fun=new&version=v2&lang=en_GB'

                    # Request confidential information
                    response = wxGet(self.session, urlredirect)
                    retCode = self._find_between(response.text, '<ret>', '</ret>')
                    self.skey = self._find_between(response.text, '<skey>', '</skey>')
                    self.wxsid = self._find_between(response.text, '<wxsid>', '</wxsid>')
                    self.wxuin = self._find_between(response.text, '<wxuin>', '</wxuin>')
                    self.pass_ticket = self._find_between(response.text, '<pass_ticket>', '</pass_ticket>')

                    if not retCode == '0':
                        break

                    if self._verbose:
                        print ('Confidential Info Retrieved:')
                        print (self.skey, self.wxsid, self.wxuin, self.pass_ticket)

                    data = {}
                    data['BaseRequest'] = {}
                    data['BaseRequest']['DeviceID'] = self.deviceID
                    data['BaseRequest']['Sid'] = self.wxsid
                    data['BaseRequest']['Skey'] = self.skey
                    data['BaseRequest']['Uin'] = self.wxuin

                    response = wxPost(
                        self.session, self._herfWXInit.format(
                            self._get_unix_timestamp(),
                            self.pass_ticket
                        ), data=data
                    )

                    self.init_info = response.json()

                    if not self.init_info['BaseResponse']['Ret'] == 0:
                        print ('Failed to init with server. Retrying...')
                        break

                    self.synckey = self.init_info['SyncKey']['List']

                    self.isLoggedIn = True
                    print ('Logged In as ' + bytes(self.init_info['User']['NickName'], 'raw_unicode_escape').decode('utf8'))
                else:
                    print (line)
                    print ('Login Failed, Retrying...')
                    break

    # Public Functions
    def run(self):
        self.isRunning = True
        while self.isRunning:
            self._request_login()
            self._request_get_contacts()
            while self.isLoggedIn:
                self._request_synccheck()
                self._fire_event('onsync', {})

    def getUserInfo(self, id):
        info = {}

        if self.contacts:
            for c in self.contacts:
                if c['UserName'] == id:
                    info = c
                    return info

        if self.init_info and self.init_info['ContactList']:
            for c in self.init_info['ContactList']:
                if c['UserName'] == id:
                    info = c
                    return info

        return info

    def sendMessage(self, toUser, content):
        data = {
            "BaseRequest":{
                "Uin": self.wxuin,
                "Sid": self.wxsid,
                "Skey": self.skey,
                "DeviceID": self.deviceID
            },"Msg":{
                "Type":1,
                "Content":content,
                "FromUserName":self.init_info['User']['UserName'],
                "ToUserName":toUser,
                "LocalID":self._get_unix_timestamp(),
                "ClientMsgId":self._get_unix_timestamp()
            }
        }

        response = wxPost(self.session, self._hrefSendMessage.format(
            self.pass_ticket
        ), payload=json.dumps(data).encode('utf8').decode('raw_unicode_escape').encode('utf8'))



        if self._verbose:
            print('Message Sent')

        resp = response.json()

        print(resp)
        return resp


    def addListener(self, event, func):
        if not event in self._listeners:
            self._listeners[event] = []
        self._listeners[event].append(func)

def wxPost(session, url, data=None, retry=10, timeout=120, payload=None, verbose=False):
    resp = None
    while not resp and retry > 0:
        try:
            if verbose:
                print ('Request Post: {}'.format(url))

            if data:
                resp = session.post(url, json=data, timeout=timeout)
            else:
                resp = session.post(url, data=payload, timeout=timeout)
        except Exception as e:
            print (e)

        retry -= 1
    return resp

def wxGet(session, url, retry=10, timeout=120,verbose=False):
    resp = None
    while not resp and retry > 0:
        try:
            if verbose:
                print ('Request Get: {}'.format(url))
            resp = session.get(url, timeout=timeout)
        except Exception as e:
            print (e)

        retry -= 1
    return resp


if __name__ == '__main__':
    print ('Runing from PyWX Module')
    import sys
    reload(sys)
    sys.setdefaultencoding('utf-8')

    bot = WXBot()
    bot.run()
