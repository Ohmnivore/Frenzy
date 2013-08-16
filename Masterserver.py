#!/usr/bin/env python2.7

import socket
import ssl
import SocketServer
import os
import sys
import urllib2
import json
from OpenSSL import SSL

ServerList = []
IPRegistry = {}

parentdir = os.path.dirname(os.path.abspath(sys.argv[0]))
sys.path.insert(0,parentdir)
mypath = os.path.normpath(os.path.dirname(os.path.abspath(sys.argv[0])))

def requestlist(connection, data):
    #connection.sendall(json.dumps(ServerList))
    print 'sent'

def addserver(connection, data):
    x = json.loads(data[1:len(data)])
    IPRegistry[connection.getsockname()] = x
    ServerList.append(IPRegistry[connection.getsockname()])
    print 'sent'

def addplayer(connection, data):
    ServerList[ServerList.index(IPRegistry[connection.getsockname()])][3] += 1
    print 'lol' + ServerList[ServerList.index(IPRegistry[connection.getsockname()])][3]

def discoplayer(connection, data):
    IPRegistry[connection][3] -= 1

messages = {
                'r' : requestlist,
                '+' : addserver,
                'a' : addplayer,
                'd' : discoplayer
}
 


def check_ip():
    pub_ip = urllib2.urlopen("http://whatismyip.com/automation/n09230945.asp").read()
    return pub_ip
#class SSlSocketServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
#
#    def __init__(self, server_address, RequestHandlerClass, bind_and_activate=True):
#        SocketServer.BaseServer.__init__(self, server_address,
#            RequestHandlerClass)
#        ctx = SSL.Context(SSL.SSLv3_METHOD)
#        cert = os.path.join(mypath, 'CERTMS.cert')
#        key = os.path.join(mypath, 'KEYMS.key')
#        #self.socket = SSL.Connection(ctx, socket.socket(self.address_family,
#        #    self.socket_type))
#        self.socket = socket.socket()
        #self.socket.setsockopt(socket.SOL_SOCKET, \
        #         socket.SO_KEEPALIVE, 1)
        #if bind_and_activate:
        #    self.server_bind()
        #    self.server_activate()
    #def shutdown_request(self,request):
    #    request.shutdown()

#class Decoder(SocketServer.StreamRequestHandler):
#    def setup(self):
#    #    self.connection = self.request
#        self.rfile = socket._fileobject(self.request, "rb", self.rbufsize)
#        self.wfile = socket._fileobject(self.request, "wb", self.wbufsize)

    def handle(self):
        #try:
        # self.request is the TCP socket connected to the client
        socket1 = self.request
        self.data = socket1.recv(1024)
        self.address = self.request
        messages[self.data[0]](self.address, self.data)
        #except:
        #    pass
#def main():
#    server = SSlSocketServer(('127.0.0.1', 9999), Decoder)
#    server.serve_forever()
class Server:
    def _init_(self, name = 'UnnamedServer', maxplayers = 8, mapname = 'Custom', gamemode = 'FFA', password = False):
        self.name = name
        self.maxplayers = maxplayers
        self.mapname = mapname
        self.gamemode = gamemode
        self.password = password
        ServerList.append(self)

class TCPHandler(SocketServer.BaseRequestHandler):
    """
    The RequestHandler class for our server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """

    def handle(self):
        #try:
        # self.request is the TCP socket connected to the client
        self.data = self.request.recvfrom(1024)
        self.address = self.client_address[0]
        messages[self.data[0][0]](self.request, self.data)
        #except:
        #    pass

if __name__ == "__main__":
    import re
    f = urllib2.urlopen("http://www.canyouseeme.org/")
    html_doc = f.read()
    f.close()
    m = re.search('(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)',html_doc)
    pub_ip = repr(m.group(0)).replace("'", "")
    print 'Public IP: ' + pub_ip

    int_ip = '192.168.1.4'#socket.gethostbyname(socket.getfqdn())
    print 'Internal IP: ' + int_ip

    HOST = int_ip
    PORT = 2000

    # Create the server
    try:
        server = SocketServer.TCPServer((pub_ip, PORT), TCPHandler)
        print 'Connected to: ' + str(pub_ip) + '    Port: 2000'
    except:
        import sys
        # prints `type(e), e` where `e` is the last exception
        print sys.exc_info()[:2]
        server = SocketServer.TCPServer((int_ip, PORT), TCPHandler)
        print 'Connected to: ' + str(int_ip) + '    Port: 2000'

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    #server.timeout = None
    server.serve_forever()