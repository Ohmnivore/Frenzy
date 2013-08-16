import sys
import socket
import threading# Import socket module
import time
import json
import os
s = socket.socket()         # Create a socket object
host = '192.168.1.4' # Get local machine name
port = 2000                # Reserve a port for your service.

ServerList = []
IPRegistry = {}

parentdir = os.path.dirname(os.path.abspath(sys.argv[0]))
sys.path.insert(0,parentdir)
mypath = os.path.normpath(os.path.dirname(os.path.abspath(sys.argv[0])))

def requestlist(connection, data):
    connection.sendall('lol')
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
 

class ClientThread(threading.Thread):
    """
    Thread checking URLs.
    """

    def __init__(self, connection):
        """
        Constructor.

        @param urls list of urls to check
        @param output file to write urls output
        """
        threading.Thread.__init__(self)
        self.connection = connection
    
    def run(self):
        """
        Thread run method. Check URLs one by one.
        """
        #pass
        time.sleep(0.01)
        #try:
        # self.request is the TCP socket connected to the client
        try:
            self.data = self.connection.recv(1024)
            messages[self.data[0]](self.connection, self.data)
        except:
            pass
        #except:
        #    pass
 
print 'Server started!'
print 'Waiting for clients...'
try:
    s.bind((host, port))        # Bind to the port
    s.listen(5)                 # Now wait for client connection.
    #c, addr = s.accept()
    #client = ClientThread(c)# Establish connection with client.
    #client.start()
    #print 'Got connection from', addr
 
    while True:
        try:
            cs, addrs = s.accept()
            cl = ClientThread(cs)# Establish connection with client.
            cl.start()
            print 'Got connection from', addr
        except:
            pass
 
except KeyboardInterrupt:
    print "closing shell..."
    s.close()
    sys.exit("Closing Application...")