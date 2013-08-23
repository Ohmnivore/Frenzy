#!/usr/bin/env python
#Frenzy Google App Engine master server source

import webapp2
import json
import datetime
from google.appengine.ext import db

ServerList = []
IPRegistry = {}
text = ''

class Server(db.Model):
    name = db.StringProperty()
    mapname = db.StringProperty()
    gamemode = db.StringProperty(choices=set(["DM", "TDM", "Z", "KOTH", "J"]))
    cp = db.IntegerProperty()
    mp = db.IntegerProperty()
    passworded = db.BooleanProperty()
    address = db.StringProperty()
    timer = db.DateTimeProperty()

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
        numbservers = 0
        ServerList = Server.all()
        for p in ServerList.run():
            if (datetime.datetime.now() - p.timer).seconds < 100:
                numbservers += 1
                text += '%(name)s|%(mapname)s|%(gm)s|%(cp)d/%(mp)d|%(pass)s<BR>' % \
                {'name':p.name,'mapname':p.mapname,'gm':p.gamemode,'cp':p.cp,'mp':p.mp,'pass':Truthify(p.passworded)}
            else:
                p.delete()
        if len(text) == 0:
            html = '<HTML><HEAD><TITLE>Frenzy master server</TITLE></HEAD><BODY><CENTER>There are no public servers at the moment.</body></HTML>'
            self.response.write(html)
        else:
            title = 'Servers online: %(number)s<BR><a href="/ip">Click here to see the IP for each server</a>' % \
            {"number": str(numbservers)}
            html = '<HTML><HEAD><TITLE>Frenzy master server</TITLE></HEAD><BODY><CENTER>%(title)s<BR>Server name|Map name|Game mode|Current players/Max players|Password required<BR>%(text)s</CENTER></body></HTML>' % \
            {'title': title, 'text': text}

            self.response.write(html)

class IPReadHandler(webapp2.RequestHandler):
    def get(self):
        global debug
        global IPRegistry, ServerList
        text = ''
        numbservers = 0
        ServerList = Server.all()
        for p in ServerList.run():
            if (datetime.datetime.now() - p.timer).seconds < 100:
                numbservers += 1
                text += '%(name)s|%(mapname)s|%(gm)s|%(cp)d/%(mp)d|%(pass)s|%(ip)s<BR>' % \
                {'name':p.name,'mapname':p.mapname,'gm':p.gamemode,'cp':p.cp,'mp':p.mp,'pass':Truthify(p.passworded),'ip':p.address}
            else:
                p.delete()
        if len(text) == 0:
            html = '<HTML><HEAD><TITLE>Frenzy master server</TITLE></HEAD><BODY><CENTER>There are no public servers at the moment.</body></HTML>'
            self.response.write(html)
        else:
            title = 'Servers online: %(number)s' % \
            {"number": str(numbservers)}
            html = '<HTML><HEAD><TITLE>Frenzy master server</TITLE></HEAD><BODY><CENTER>%(title)s<BR>Server name|Map name|Game mode|Current players/Max players|Password required|IP<BR>%(text)s</CENTER></body></HTML>' % \
            {'title': title, 'text': text}

            self.response.write(html)

class ReadHandler(webapp2.RequestHandler):
    def get(self):
        ServerList = Server.all()
        if ServerList.count(limit=1) == 0:
            self.response.write('')
        else:
            servers = []
            for x in ServerList.run():
                if (datetime.datetime.now() - x.timer).seconds < 100:
                    server = [x.name,x.mapname,x.gamemode,x.cp,x.mp,Truthify(x.passworded),x.address]
                    servers.append(server)
                else:
                    x.delete()
            self.response.write(json.dumps(servers))

class ServerHandler(webapp2.RequestHandler):
    def post(self):
        ip = self.request.remote_addr
        cmd = self.request.get('cmd')
        duplicate = False
        if cmd == '+':
            for server in Server.all().run():
                if server.address == ip:
                    duplicate = True
            if duplicate == False:
                ##try:
                x = json.loads(self.request.get('info'))
                x.append(ip)
                serverx = Server()
                serverx.name, serverx.mapname, serverx.gamemode, serverx.cp, serverx.mp, serverx.passworded, serverx.address = x
                serverx.timer = datetime.datetime.now()
                serverx.put()
        if cmd == '-':
            query = db.GqlQuery("SELECT * FROM Server WHERE address = :1", ip)
            #server = IPRegistry[ip].get()
            server = query.get()
            server.delete()
        if cmd == '+p':
            query = db.GqlQuery("SELECT * FROM Server WHERE address = :1", ip)
            server = query.get()
            #server = IPRegistry[ip].get()
            server.cp += 1
            server.put()
        if cmd == '-p':
            query = db.GqlQuery("SELECT * FROM Server WHERE address = :1", ip)
            #server = IPRegistry[ip].get()
            server = query.get()
            server.cp -= 1
            server.put()
        if cmd == 'h':
            query = db.GqlQuery("SELECT * FROM Server WHERE address = :1", ip)
            server = query.get()
            server.timer = datetime.datetime.now()


app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/read', ReadHandler),
    ('/server', ServerHandler),
    ('/ip', IPReadHandler)
]) #, debug=True])
