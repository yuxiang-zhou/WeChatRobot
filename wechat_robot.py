# coding=utf8

from flask import Flask
from flask import render_template, send_file
# from flask_restful import Resource, Api
from pywx import WXBot
import time
import threading
import json
import requests
import urllib

bot = WXBot(verbose=True)
wechat_thread = None
# helper functions
def tulingReply(text, id=None):
    key = '56bbd71ded658acbd04169a21b605114'
    strRequest = 'http://www.tuling123.com/openapi/api?key={}&info={}'.format(
        key,text
    )

    if id:
        strRequest = '{}&userid={}'.format(strRequest, id.replace('@',''))

    r = requests.get(
        strRequest
    )
    return r.json()

# wechat bot configuration
def onMessage(msg):

    fromUser = msg['FromUserName']
    toUser = msg['ToUserName']

    fromInfo = bot.getUserInfo(fromUser)
    toInfo = bot.getUserInfo(toUser)

    fromNickName = fromInfo['NickName'] if fromInfo else fromUser
    toNickName = toInfo['NickName'] if toInfo else toUser
    fromRemarkName = fromInfo['RemarkName'] if fromInfo else fromUser
    toRemarkName = toInfo['RemarkName'] if toInfo else toUser

    print ('({}) {}({}) - {}({}): {}'.format(
        msg['MsgType'],
        fromNickName.encode('raw_unicode_escape').decode('utf8'),
        fromRemarkName.encode('raw_unicode_escape').decode('utf8'),
        toNickName.encode('raw_unicode_escape').decode('utf8'),
        toRemarkName.encode('raw_unicode_escape').decode('utf8'),
        msg['Content'].encode('raw_unicode_escape').decode('utf8')
    ))
bot.addListener('onmessage',onMessage)


autoReply = {}
def onGFMessage(msg):
    automsg = '苗宝宝主人好～这里是Crystal自动应答系统Alpha-1.0~猪宝宝主人暂时不在，收到消息后会联系苗宝宝主人的～（猪宝宝留言：老公永远都只爱老婆～）'
    reply_gap = 1800
    timestamp = bot._get_unix_timestamp()

    fromUser = msg['FromUserName']
    toUser = msg['ToUserName']
    msgtype = msg['MsgType']
    content = msg['Content'].encode('raw_unicode_escape')

    fromInfo = bot.getUserInfo(fromUser)
    toInfo = bot.getUserInfo(toUser)

    fromNickName = fromInfo['NickName'] if fromInfo else fromUser
    toNickName = toInfo['NickName'] if toInfo else toUser
    fromRemarkName = fromInfo['RemarkName'] if fromInfo else fromUser
    toRemarkName = toInfo['RemarkName'] if toInfo else toUser

    def isMessageFromGroup():
        if 'MemberList' in fromInfo and fromInfo['MemberList']:
            return True
        elif fromUser.count('@') > 1:
            return True
        return False

    if not isMessageFromGroup():
        if (
            not fromUser in autoReply or
            (not 'replyed' in autoReply[fromUser] and
                timestamp - autoReply[fromUser]['timestamp'] > reply_gap)):
            autoReply[fromUser] = {'replyed':True}
            if fromRemarkName.encode('raw_unicode_escape') == '老婆':
                print ('Important Message!!!')
                bot.sendMessage(fromUser, automsg)
            else:
                bot.sendMessage(fromUser, '这里是Crystal-Alpha-1.0自动应答助手，主人暂时不在，有事请留言。')
        elif (not 'timestamp' in autoReply[fromUser] or
            timestamp - autoReply[fromUser]['timestamp'] > reply_gap) and not fromUser == bot.init_info['User']['UserName'] and not fromInfo['MemberList'] and fromUser.count('@') > 0:
            reply = tulingReply(content,fromUser)
            bot.sendMessage(fromUser, 'Crystal自动应答:{}'.format(reply['text'].encode('utf8')))
            if reply['code'] == 308000:
                for menu in reply['list']:
                    bot.sendMessage(fromUser, 'Crystal自动应答:{}'.format(menu['name'].encode('utf8')))
                    bot.sendMessage(fromUser, 'Crystal自动应答:{}'.format(menu['info'].encode('utf8')))
                    bot.sendMessage(fromUser, 'Crystal自动应答:{}'.format(menu['detailurl'].encode('utf8')))
            elif reply['code'] == 302000:
                for news in reply['list']:
                    bot.sendMessage(fromUser, 'Crystal自动应答:{}'.format(news['article'].encode('utf8')))
                    bot.sendMessage(fromUser, 'Crystal自动应答:{}'.format(news['detailurl'].encode('utf8')))
            elif reply['code'] == 305000:
                for ticket in reply['list']:
                    bot.sendMessage(fromUser, 'Crystal自动应答:{}: {}({}) -> {}({}) '.format(
                        ticket['trainnum'].encode('utf8'),
                        ticket['start'].encode('utf8'),
                        ticket['starttime'].encode('utf8'),
                        ticket['terminal'].encode('utf8'),
                        ticket['endtime'].encode('utf8'),
                    ))
                    bot.sendMessage(fromUser, 'Crystal自动应答:{}'.format(ticket['detailurl'].encode('utf8')))
            elif reply['code'] == 306000:
                for ticket in reply['list']:
                    bot.sendMessage(fromUser, 'Crystal自动应答:{}: {} - {}'.format(
                        ticket['flight'].encode('utf8'),
                        ticket['starttime'].encode('utf8'),
                        ticket['endtime'].encode('utf8')
                    ))
            else:
                pass

    if msgtype == 51:
        autoReply[toUser] = {'timestamp':timestamp}

# bot.addListener('onmessage',onGFMessage)

app = Flask(__name__)


# RESTful API configuration
@app.route('/api/start')
def startWechat():
    if not wechat_thread.isAlive():
        wechat_thread.start()
        return 'Starting WeChat Bot'
    else:
        return 'Bot Started Already'

@app.route('/api/init_info')
def statusWechat():
    return json.dumps(bot.init_info)

@app.route('/api/loginstatus')
def loginStatusWechat():
    data = {}
    data['login'] = bot.isLoggedIn
    data['status'] = bot.status
    data['avatar'] = bot.avatar
    return json.dumps(data)

@app.route('/api/qr')
def qrWechat():
    return bot.hrefQR

@app.route('/api/replystatus')
def replystatusWechat():
    return json.dumps(autoReply)

@app.route('/api/contacts')
def contactsWechat():
    return json.dumps(bot.contacts)

@app.route('/api/sendtestmsg')
def sendtestWechat():
    json.dumps(bot.sendMessage('filehelper','测试'))
    return 'test'

# UI configuration

@app.route('/')
def index():
    return send_file('templates/index.html')

if __name__ == '__main__':
    if not wechat_thread:
        wechat_thread = threading.Thread(target=bot.run)
        wechat_thread.daemon = True

    app.run(debug=True)
