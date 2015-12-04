import subprocess
import requests
import pytz, calendar
from datetime import datetime

# def send_msg(user, msg):
#     # subprocess.call([
#     #     'curl',
#     #     'https://wx.qq.com/cgi-bin/mmwebwx-bin/webwxsendmsg?lang=en',
#     #     '-H','Pragma: no-cache',
#     #     '-H','Origin: https://wx.qq.com',
#     #     '-H','Accept-Encoding: gzip, deflate',
#     #     '-H','Accept-Language: en-GB,en-US;q=0.8,en;q=0.6,it;q=0.4,zh-CN;q=0.2,zh-TW;q=0.2',
#     #     '-H','User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/45.0.2454.85 Chrome/45.0.2454.85 Safari/537.36',
#     #     '-H','Content-Type: application/json;charset=UTF-8',
#     #     '-H','Accept: application/json, text/plain, */*',
#     #     '-H','Cache-Control: no-cache',
#     #     '-H','Referer: https://wx.qq.com/?&lang=en',
#     #     '-H','Cookie: pgv_pvi=527265792; pgv_si=s4686718976; webwxuvid=41149120bbcb969003f03a6570e9d825415744f2855360e73cd06ec38bd4d4dd5e79f37df5a8a75e6dd6f555d770f2a1; pgv_info=ssid=s2492421533; pgv_pvid=6972363959; pt_clientip=fe2e7f0000015683; pt_serverip=f41e0af17164240f; mm_lang=en; MM_WX_NOTIFY_STATE=1; MM_WX_SOUND_STATE=1; wxpluginkey=1449142753; wxuin=300781955; wxsid=HVTz77loQGRIylWs; webwx_data_ticket=AQacPwS+o07YAaQ8OVi6OwLJ',
#     #     '-H','Connection: keep-alive',
#     #     '--data-binary',
#     #     '$\'{"BaseRequest":{"Uin":300781955,"Sid":"HVTz77loQGRIylWs","Skey":"@crypt_c39a9d8a_29735d46464e289c60d22e867baecd68","DeviceID":"e368943473324180"},"Msg":{"Type":1,"Content":"'+msg+'","FromUserName":"@44052695e3776afd39c1e0a86da623be","ToUserName":"@4713352c6663bca8550b62447b1d731e9600961dbba9f3b5a95e85e3765273a1","LocalID":"14491525566330008","ClientMsgId":"14491525566330008"}}\'',
#     #     '--compressed'])
#     subprocess.call(['curl',' \'https://wx.qq.com/cgi-bin/mmwebwx-bin/webwxsendmsg?lang=en\' -H \'Pragma: no-cache\' -H \'Origin: https://wx.qq.com\' -H \'Accept-Encoding: gzip, deflate\' -H \'Accept-Language: en-GB,en-US;q=0.8,en;q=0.6,it;q=0.4,zh-CN;q=0.2,zh-TW;q=0.2\' -H \'User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/45.0.2454.85 Chrome/45.0.2454.85 Safari/537.36\' -H \'Content-Type: application/json;charset=UTF-8\' -H \'Accept: application/json, text/plain, */*\' -H \'Cache-Control: no-cache\' -H \'Referer: https://wx.qq.com/?&lang=en\' -H \'Cookie: pgv_pvi=527265792; pgv_si=s4686718976; webwxuvid=41149120bbcb969003f03a6570e9d825415744f2855360e73cd06ec38bd4d4dd5e79f37df5a8a75e6dd6f555d770f2a1; pgv_info=ssid=s2492421533; pgv_pvid=6972363959; pt_clientip=fe2e7f0000015683; pt_serverip=f41e0af17164240f; mm_lang=en; MM_WX_NOTIFY_STATE=1; MM_WX_SOUND_STATE=1; wxpluginkey=1449142753; wxuin=300781955; wxsid=HVTz77loQGRIylWs; webwx_data_ticket=AQacPwS+o07YAaQ8OVi6OwLJ\' -H \'Connection: keep-alive\' --data-binary $\'{"BaseRequest":{"Uin":300781955,"Sid":"HVTz77loQGRIylWs","Skey":"@crypt_c39a9d8a_29735d46464e289c60d22e867baecd68","DeviceID":"e368943473324180"},"Msg":{"Type":1,"Content":"\u8001\u5a46\u4e56\uff5e","FromUserName":"@44052695e3776afd39c1e0a86da623be","ToUserName":"@4713352c6663bca8550b62447b1d731e9600961dbba9f3b5a95e85e3765273a1","LocalID":"14491525566330008","ClientMsgId":"14491525566330008"}}\' --compressed'])
#
# /jslogin?appid=wx782c26e4c19acffb&redirect_uri=https%3A%2F%2Fwx.qq.com%2Fcgi-bin%2Fmmwebwx-bin%2Fwebwxnewloginpage&fun=new&lang=en_GB&_=1449166664291

class WXBot(object):

    def __init__(self):
        # Predefine request strings
        self._hrefLoginFormat = 'https://wx.qq.com/jslogin?appid=wx782c26e4c19acffb&redirect_uri=https%3A%2F%2Fwx.qq.com%2Fcgi-bin%2Fmmwebwx-bin%2Fwebwxnewloginpage&fun=new&lang=en_GB&_={}'

        self._hrefQRCodeFormat = 'https://login.weixin.qq.com/qrcode/{}'

        self._herfScanFormat = 'https://login.weixin.qq.com/cgi-bin/mmwebwx-bin/login?loginicon=true&uuid={}&tip=0&r=-1832847261&_={}'

        self._herfWXInit = 'https://wx.qq.com/cgi-bin/mmwebwx-bin/webwxinit?r=-1832847261&lang=en_GB&pass_ticket={}'

        self._hrefWXGetContacts = 'https://wx.qq.com/cgi-bin/mmwebwx-bin/webwxgetcontact?lang=en_GB&pass_ticket={}&r={}&skey={}'

        self._hrefSynccheck =  'https://webpush.weixin.qq.com/cgi-bin/mmwebwx-bin/synccheck?r={}&skey={}&sid={}&deviceid={}&synckey={}'

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
        response = self.session.get(self._hrefWXGetContacts.format(
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

        response = self.session.get(self._hrefSynccheck.format(
            self._get_unix_timestamp(),
            self.skey,
            self.wxsid,
            self.deviceID,
            format_synckey()
        ))

        selector = self._find_between(response.text,'selector:"','"}')

        if selector is '0':
            # increment key 1000 by 1
            for k in self.synckey:
                if k['Key'] == 1000:
                    k['Val'] += 1
        else:
            # Get New Messages
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

            response = self.session.post(self._hrefWebwxsync.format(
                self.wxsid,
                self.skey,
                self.pass_ticket
            ), json=data)

            print 'Message Recieved:'
            print response.json()


    def request_login(self):
        while(not self.isLoggedIn):
            response = self.session.get(self._hrefLoginFormat.format(self._get_unix_timestamp()))

            self.uuid = self._find_between(response.text,'uuid = \"',"\";")

            print self._hrefQRCodeFormat.format(self.uuid)

            # wait for scan
            while(not self.isLoggedIn):
                response = self.session.get(
                    self._herfScanFormat.format(
                        self.uuid, self._get_unix_timestamp()
                    )
                )
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
                    response = self.session.get(urlredirect)
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

                    response = self.session.post(
                        self._herfWXInit.format(self.pass_ticket),
                        json=data
                    )
                    print response.text
                    self.init_info = response.json()

                    if not self.init_info['BaseResponse']['Ret'] == 0:
                        print 'Failed to init with server. Retrying...'
                        break

                    self.synckey = data['SyncKey']['List']

                    self.isLoggedIn = True
                    print 'Logged In as ' + self.init_info['User']['NickName']
                else:
                    print line
                    print 'Login Failed, Retrying...'
                    break

    def run(self):
        self.request_login()

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


if __name__ == '__main__':
    bot = WXBot()
    bot.run()
