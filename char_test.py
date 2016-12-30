# encodeing=utf8
str_test = '\xe4\xb8\xad\xe6\x96\x87\xe6\xb5\x8b\xe8\xaf\x95'
str_testu = u'\xe4\xb8\xad\xe6\x96\x87\xe6\xb5\x8b\xe8\xaf\x95'

print '{}'.format(str_test)
print '{}'.format(str_testu.encode('raw_unicode_escape'))

import urllib

content = '&lt;msg&gt;<br/>&lt;op id=\'2\'&gt;<br/>&lt;username&gt;filehelper&lt;/username&gt;<br/>&lt;/op&gt;<br/>&lt;/msg&gt;'


print urllib.quote_plus(content.encode('raw_unicode_escape'))
print urllib.unquote_plus(urllib.quote_plus(content.encode('raw_unicode_escape')))



import requests, datetime, pytz, calendar, json

def wxPost(session, url, data=None, retry=10, timeout=120, payload=None, verbose=False):
    resp = None
    while not resp and retry > 0:
        try:
            if verbose:
                print 'Request Post: {}'.format(url)

            if data:
                resp = session.post(url, json=data, timeout=timeout)
            else:
                resp = session.post(url, data=payload, timeout=timeout)
        except Exception as e:
            print e

        retry -= 1
    return resp

def _get_unix_timestamp(time_zone='UTC'):
    dt = datetime.datetime.now()
    tz = pytz.timezone(time_zone)
    utc_dt = tz.localize(dt, is_dst=True).astimezone(pytz.utc)
    return calendar.timegm(utc_dt.timetuple())

wxuin = 300781955
wxsid = 'JJ1y+p70phJRcE+u'
skey = '@crypt_c39a9d8a_f15934a7a3a2336abd7aabb4696050a9'
deviceID = 'e197136774891987'
content = '再测试一下'
fromuserid = '@02ac44d2983636911e5e4281a0374326'
toUserid = 'filehelper'
pass_ticket = 'JUV5n3uZAwzU%252B3mPFzYlvvBkLXZ0DFZqEeywIhI8Va47%252F0sa%252F4MnLy3X0qpJY%252FHo'

data = {
            "BaseRequest":{
                "Uin": wxuin,
                "Sid": wxsid,
                "Skey": skey,
                "DeviceID": deviceID
            },"Msg":{
                "Type":1,
                "Content":content,
                "FromUserName":fromuserid,
                "ToUserName":toUserid,
                "LocalID":_get_unix_timestamp(),
                "ClientMsgId":_get_unix_timestamp()
            }
        }



_hrefSendMessage = 'https://wx.qq.com/cgi-bin/mmwebwx-bin/webwxsendmsg?lang=en_GB&pass_ticket={}'

response = requests.post(_hrefSendMessage.format(
    pass_ticket
), data=json.dumps(data).decode('raw_unicode_escape').encode('utf8'))

resp = response.json()

print resp

json.dumps(data).decode('raw_unicode_escape').decode('utf8')

import urllib2

session = requests.Session()
headers = {
            'Pragma': 'no-cache',
            'Origin': 'http://www.niurenqushi.com',
            'Accept-Language': 'en-GB,en-US;q=0.8,en;q=0.6,it;q=0.4,zh-CN;q=0.2,zh-TW;q=0.2',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/45.0.2454.85 Chrome/45.0.2454.85 Safari/537.36',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Accept': '*/*',
            'Cache-Control': 'no-cache',
            'Referer': 'http://www.niurenqushi.com/app/simsimi/',
            'X-Requested-With': 'XMLHttpRequest',

        }
session.headers.update(headers)

text='去厕所干嘛'
r = requests.get('http://www.tuling123.com/openapi/api?key=56bbd71ded658acbd04169a21b605114&info={}'.format(text))
print '{}'.format(r.json()['text'].encode('utf8'))
print r.json()

struct = {'test':123}

struct.pop('test')



shapes= []
for i in mio.import_images('/homes/yz4009/wd/databases/sketch_trained/fork/svs'):
    shapes.append(i)

A,e = rpca_alm(as_matrix(shapes))

ears = []
for i in mio.import_images('/homes/yz4009/wd/databases/ear/200EW/*_l.*', max_images=80):
    pc = i.landmarks['PTS'].lms
    pc.centre_of_bounds()
    ears.append(i.crop_to_landmarks(boundary=30).rescale_to_diagonal(150))

visualize_images(ears)

minh, minw = np.min(np.array([i.shape for i in ears]),axis=0)

minh, minw

cropped_ear = []
for i in ears:
    h,w = i.shape
    dh = (h - minh) / 2
    dw = (w - minw) / 2
    if i.n_channels > 1:
        i = i.as_greyscale()
    cropped_ear.append(i.crop([dh,dw],[dh+minh,dw+minw]))

visualize_images(cropped_ear)

from dAAMs.rpca import rpca_alm, rpca_pcp

A,E = rpca_pcp(data, 0.02)

np.linalg.matrix_rank(A)

temp = cropped_ear[0]

rpca_img = [temp.copy().from_vector(i) for i in A]

visualize_images(rpca_img)


# import time
# import threading
#
# class TClass(object):
#     def __init__(self):
#         self.id = 123;
#
#     def run(self):
#         while True:
#             print self.id
#             time.sleep(1)
#
# data = TClass()
#
# t = threading.Thread(target=data.run)
# t.daemon = True
# t.start()
#
# print 'before change id'
# time.sleep(5)
# print 'change id to 100'
# data.id = 100
# time.sleep(5)
# print 'end of main'
