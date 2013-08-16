#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
import json

ServerList = []
IPRegistry = {}
text = ''
debug = 0

def Truthify(boolean):
    try:
        if boolean == True:
            return 'Yes'
        else:
            return 'No'
    except:
        return ''

class MainHandler(webapp2.RequestHandler):
    def get(self):
        global debug
        global IPRegistry, ServerList
        text = ''
        for x in ServerList:
            text += '%(name)s|%(mapname)s|%(gm)s|%(cp)d/%(mp)d|%(pass)s<BR>' % \
            {'name':str(x[0]),'mapname':str(x[1]),'gm':x[2],'cp':x[3],'mp':x[4],'pass':Truthify(x[5])}
        if len(text) == 0:
            html = '<HTML><HEAD><TITLE>Frenzy master server</TITLE></HEAD><BODY><CENTER>There are no public servers at the moment.</body></HTML>'
            self.response.write(html)
        else:
            title = 'Servers online: %(number)s<BR><a href="/ip">Click here to see the IP for each server</a>' % \
            {"number": str(len(ServerList))}
            html = '<HTML><HEAD><TITLE>Frenzy master server</TITLE></HEAD><BODY><CENTER>%(title)s<BR>Server name|Map name|Game mode|Current players/Max players|Password required<BR>%(text)s</CENTER></body></HTML>' % \
            {'title': title, 'text': text}

            self.response.write(html)

class IPReadHandler(webapp2.RequestHandler):
    def get(self):
        global debug
        global IPRegistry, ServerList
        text = ''
        for x in ServerList:
            text += '%(name)s|%(mapname)s|%(gm)s|%(cp)d/%(mp)d|%(pass)s|%(ip)s<BR>' % \
            {'name':str(x[0]),'mapname':str(x[1]),'gm':x[2],'cp':x[3],'mp':x[4],'pass':Truthify(x[5]),'ip':x[6]}
        if len(text) == 0:
            html = '<HTML><HEAD><TITLE>Frenzy master server</TITLE></HEAD><BODY><CENTER>There are no public servers at the moment.</body></HTML>'
            self.response.write(html)
        else:
            title = 'Servers online: %(number)s' % \
            {"number": str(len(ServerList))}
            html = '<HTML><HEAD><TITLE>Frenzy master server</TITLE></HEAD><BODY><CENTER>%(title)s<BR>Server name|Map name|Game mode|Current players/Max players|Password required|IP<BR>%(text)s</CENTER></body></HTML>' % \
            {'title': title, 'text': text}

            self.response.write(html)

class ReadHandler(webapp2.RequestHandler):
    def get(self):
        if len(ServerList) == 0:
            self.response.write('')
        else:
            self.response.write(json.dumps(ServerList))

class ServerHandler(webapp2.RequestHandler):
    def post(self):
        global debug
        global IPRegistry, ServerList
        debug += 1
        ip = self.request.remote_addr
        cmd = self.request.get('cmd')
        duplicate = False
        if cmd == '+':
            for key in IPRegistry.keys():
                if key == ip:
                    duplicate = True
            if duplicate == False:
                #self.response.write('Lol')
                try:
                    x = json.loads(self.request.get('info'))
                    #if len(x) == 6 and x[0] is str == True and x[1] is str == True and x[2] is str == True and x[3] is int == True and x[4] is int == True:
                    x.append(ip)
                    IPRegistry[ip] = x
                    ServerList.append(IPRegistry[ip])
                except:
                    pass
        if cmd == '-':
            for server in ServerList:
                if server[6] == ip:
                    del IPRegistry[server[6]]
                    ServerList.remove(server)
        if cmd == '+p':
            for server in ServerList:
                if server[6] == ip:
                    server[3] += 1
        if cmd == '-p':
            for server in ServerList:
                if server[6] == ip:
                    server[3] -= 1


app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/read', ReadHandler),
    ('/server', ServerHandler),
    ('/ip', IPReadHandler)
], debug=True)
