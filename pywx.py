import subprocess
import cookielib
import urllib
import urllib2
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
        # Initialise Browser
        self.cj = cookielib.CookieJar()
        self.opener = urllib2.build_opener(
            urllib2.HTTPRedirectHandler(),
            urllib2.HTTPHandler(debuglevel=0),
            urllib2.HTTPSHandler(debuglevel=0),
            urllib2.HTTPCookieProcessor(self.cj)
        )
        self.opener.addheaders = [
            ('User-agent', 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/45.0.2454.85 Chrome/45.0.2454.85 Safari/537.36')
        ]
        self.opener.addheaders = [
            ('Connection', 'keep-alive')
        ]
        self.opener.addheaders = [
            ('Pragma', 'no-cache')
        ]
        self.opener.addheaders = [
            ('Cache-Control', 'no-cache')
        ]
        self.opener.addheaders = [
            ('Accept-Encoding', 'gzip, deflate, sdch')
        ]
        self.opener.addheaders = [
            ('Accept-Language', 'en-GB,en-US;q=0.8,en;q=0.6,it;q=0.4,zh-CN;q=0.2,zh-TW;q=0.2')
        ]

        # Predefine request strings
        self._hrefLoginFormat = 'https://wx.qq.com/jslogin?appid=wx782c26e4c19acffb&redirect_uri=https%3A%2F%2Fwx.qq.com%2Fcgi-bin%2Fmmwebwx-bin%2Fwebwxnewloginpage&fun=new&lang=en_GB&_={}'

        self._hrefQRCodeFormat = 'https://login.weixin.qq.com/qrcode/{}'

        self._herfScanFormat = 'https://login.weixin.qq.com/cgi-bin/mmwebwx-bin/login?loginicon=true&uuid={}&tip=0&r=-1765867164&_={}'

        # global variables
        self.isLoggedIn = False
        self.uuid = ""

    def request_login(self):
        response = self.opener.open(self._hrefLoginFormat.format(self._get_unix_timestamp()))

        self.uuid = self._find_between(response.readlines()[0],'uuid = \"',"\";")

        print self._hrefQRCodeFormat.format(self.uuid)

        # wait for scan
        while(not self.isLoggedIn):
            response = self.opener.open(
                self._herfScanFormat.format(
                    self.uuid, self._get_unix_timestamp()
                )
            )

            print response.readlines()

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
