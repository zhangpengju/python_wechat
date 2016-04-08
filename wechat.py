#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

import tornado.ioloop
import tornado.web
import hashlib
import commands
import xml.etree.ElementTree as ET
import time

def check_signature(signature, timestamp, nonce):
    args = []
    # 微信公众平台里输入的token
    args.append('linden')
    args.append(timestamp)
    args.append(nonce)
    args.sort()
    mysig = hashlib.sha1(''.join(args)).hexdigest()
    return mysig == signature

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        signature = self.get_argument('signature')
        timestamp = self.get_argument('timestamp')
        nonce = self.get_argument('nonce')
        echostr = self.get_argument('echostr')
        if check_signature(signature, timestamp, nonce):
            self.write(echostr)
        else:
            self.write('fail')
    def post(self): 
        body = self.request.body
        data = ET.fromstring(body)
        toUser = data.find('ToUserName').text
        fromUser = data.find('FromUserName').text
        msgType = data.find('MsgType').text
        content = data.find('Content').text
        textTpl = """<xml>
            <ToUserName><![CDATA[%s]]></ToUserName>
            <FromUserName><![CDATA[%s]]></FromUserName>
            <CreateTime>%s</CreateTime>
            <MsgType><![CDATA[%s]]></MsgType>
            <Content><![CDATA[%s]]></Content>
            </xml>"""
        out = textTpl % (fromUser, toUser, str(int(time.time())), msgType, content)
        self.write(out)
        
application = tornado.web.Application([
    (r"/", MainHandler),
])

if __name__ == "__main__":
    application.listen(80)
    tornado.ioloop.IOLoop.instance().start()