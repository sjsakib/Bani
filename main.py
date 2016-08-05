import web
from routines import *
import json

urls = (
    '/','index',
    '/hook','Hook'
)

class index:
    def GET(self):
        return "You have nothing to do here."


class Hook:
    def GET(self):
        req = web.input()
        try:
            if(req['hub.verify_token'] == '****'):
                return req['hub.challenge']
            else:
                return 'Wrong Token'
        except:
            return '400'

    def POST(self):
        data = json.loads(web.data())
        try:
            sender  = data['entry'][0]['messaging'][0]['sender']['id']
            message = data['entry'][0]['messaging'][0]['message']['text']
            respond(sender,message)
        except:
            pass
        return 'ok'



application = web.application(urls,globals(),autoreload=False).wsgifunc()