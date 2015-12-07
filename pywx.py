import subprocess
import requests
import pytz, calendar, time
from datetime import datetime

class WXBot(object):

    def __init__(self):
        # Predefine request strings
        self._hrefLoginFormat = 'https://wx.qq.com/jslogin?appid=wx782c26e4c19acffb&redirect_uri=https%3A%2F%2Fwx.qq.com%2Fcgi-bin%2Fmmwebwx-bin%2Fwebwxnewloginpage&fun=new&lang=en_GB&_={}'

        self._hrefQRCodeFormat = 'https://login.weixin.qq.com/qrcode/{}'

        self._herfScanFormat = 'https://login.weixin.qq.com/cgi-bin/mmwebwx-bin/login?loginicon=true&uuid={}&tip=0&r=-1832847261&_={}'

        self._herfWXInit = 'https://wx.qq.com/cgi-bin/mmwebwx-bin/webwxinit?r=-1832847261&lang=en_GB&pass_ticket={}'

        self._hrefWXGetContacts = 'https://wx.qq.com/cgi-bin/mmwebwx-bin/webwxgetcontact?lang=en_GB&pass_ticket={}&r={}&skey={}'

        self._hrefSynccheck =  'https://webpush.weixin.qq.com/cgi-bin/mmwebwx-bin/synccheck?r={}&skey={}&sid={}&uin={}&deviceid={}&synckey={}&_={}'

        self._hrefWebwxsync = 'https://wx.qq.com/cgi-bin/mmwebwx-bin/webwxsync?sid={}&skey={}&lang=en_GB&pass_ticket={}'

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
        self.uuid = ""
        self.skey = ""
        self.wxsid = ""
        self.wxuin = ""
        self.deviceID = 'e048677534097806'
        self.pass_ticket = ""
        self.contacts = []
        self.synckey = []

        # Session Management
        self.session = requests.Session()
        self.session.headers.update(self.headers)

    def request_get_contacts(self):
        response = wxGet(self.session, self._hrefWXGetContacts.format(
            self.pass_ticket,
            self._get_unix_timestamp(),
            self.skey
        ))

        data = response.json()
        if data['BaseResponse']['Ret'] == 0:
            self.contacts = data['MemberList']
        else:
            print 'Failed to get contacts list.'

    def request_synccheck(self):

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

        selector = self._find_between(response.text,'selector:"','"}')

        print 'Sync Check Done:'
        print selector
        print response.text

        if selector == "0" or selector == 0:
            print 'Status Idel'
        else:
            # Get New Messages
            print self.request_get_update()

    def request_get_update(self):
        data = {
            "BaseRequest":{
                "Uin": self.wxuin,
                "Sid": self.wxsid,
                "Skey": self.skey,
                "DeviceID": self.deviceID
            },"SyncKey":{
                "Count":len(self.synckey),
                "List":self.synckey
            },"rr":-1851102809
        }

        response = wxPost(self.session, self._hrefWebwxsync.format(
            self.wxsid,
            self.skey,
            self.pass_ticket
        ), data=data)

        print 'Message Recieved:'
        data = response.json()

        self.synckey = data['SyncKey']['List']
        return data

    def request_login(self):
        while(not self.isLoggedIn):

            response = wxGet(self.session, self._hrefLoginFormat.format(self._get_unix_timestamp()))

            self.uuid = self._find_between(response.text,'uuid = \"',"\";")

            print self._hrefQRCodeFormat.format(self.uuid)

            # wait for scan
            while(not self.isLoggedIn):
                response = wxGet(self.session, self._herfScanFormat.format(
                    self.uuid, self._get_unix_timestamp()
                ))

                if not response:
                    break

                line = response.text
                code = self._find_between(line, 'window.code=', ';')
                if code == "408":
                    print "Please Scan QR Code"
                elif code == '201':
                    print "Please accept login on your phone"
                elif code == '200':
                    print 'Initialising...'

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

                    print 'Confidential Info Retrieved:'
                    print self.skey, self.wxsid, self.wxuin, self.pass_ticket

                    data = {}
                    data['BaseRequest'] = {}
                    data['BaseRequest']['DeviceID'] = self.deviceID
                    data['BaseRequest']['Sid'] = self.wxsid
                    data['BaseRequest']['Skey'] = self.skey
                    data['BaseRequest']['Uin'] = self.wxuin

                    response = wxPost(
                        self.session, self._herfWXInit.format(self.pass_ticket), data=data
                    )

                    self.init_info = response.json()

                    if not self.init_info['BaseResponse']['Ret'] == 0:
                        print 'Failed to init with server. Retrying...'
                        break

                    self.synckey = self.init_info['SyncKey']['List']

                    self.isLoggedIn = True
                    print 'Logged In as ' + self.init_info['User']['NickName']
                else:
                    print line
                    print 'Login Failed, Retrying...'
                    break

    def run(self):
        self.request_login()
        while True:
            self.request_synccheck()

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


def wxPost(session, url, data=None, retry=10):
    resp = None
    while not resp and retry > 0:
        try:
            print 'Request Post: {}'.format(url)
            resp = session.post(url, json=data)
        except Exception as e:
            print e

        retry -= 1
    return resp

def wxGet(session, url, retry=10):
    resp = None
    while not resp and retry > 0:
        try:
            print 'Request Get: {}'.format(url)
            resp = session.get(url)
        except Exception as e:
            print e

        retry -= 1
    return resp


if __name__ == '__main__':
    bot = WXBot()
    bot.run()
