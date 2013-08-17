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

client = legume.Client()
client.connect((open(os.path.join(mypath, 'ClientIP.txt'), 'r').read(), 6385))

legume.messages.message_factory.add(SampleMessage)

clientold = False

while True:
    client.update()
    if client.connected == True and clientold != True:
        print 'Connected successfuly!'
        SampleMsg = SampleMessage()
        SampleMsg.placeholder.value = 'placeholder'
        client.send_reliable_message(SampleMsg)
        clientold = client.connected