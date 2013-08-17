import legume
import sys
import os

def we_are_frozen():
    """Returns whether we are frozen via py2exe.
    This will affect how we find out where we are located."""

    return hasattr(sys, "frozen")


def module_path():
    """ This will get us the program's directory,
    even if we are frozen using py2exe"""

    if we_are_frozen():
        return os.path.dirname(unicode(sys.executable, sys.getfilesystemencoding( )))

    return os.path.dirname(unicode(__file__, sys.getfilesystemencoding( )))

mypath = module_path()

class SampleMessage(legume.messages.BaseMessage):
    MessageTypeID = legume.messages.BASE_MESSAGETYPEID_USER+1
    MessageValues ={
    'placeholder': 'string 20'
    }

server = legume.Server()
server.listen((open(os.path.join(mypath, 'ServerIP.txt'), 'r').read(), 6385))

def custom_msghandler(sender, message):
    if message.MessageTypeID == SampleMessage.MessageTypeID:
        print 'New guy connected from: ' + str(sender.address)

server.OnMessage += custom_msghandler

legume.messages.message_factory.add(SampleMessage)

while True:
    server.update()