#!/usr/bin/env python2.7
import os
#os.environ['KIVY_IMAGE'] = 'pil'
import kivy
kivy.require('1.6.0')
from kivy.config import Config
Config.set('graphics', 'width', '450')
Config.set('graphics', 'height', '400')
Config.set('graphics','resizable',0) 
import pickle
import kivy, socket, sys, random, inspect, twisted
kivy.require('1.6.0')
from kivy.config import Config
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.stacklayout import StackLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.properties import ObjectProperty, StringProperty, DictProperty, NumericProperty, ListProperty
from kivy.clock import Clock
from kivy.uix.widget import Widget
from kivy.uix.gridlayout import GridLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.factory import Factory
from kivy.logger import Logger

#import socket
#import SocketServer
import subprocess

mypath = os.path.normpath(os.path.dirname(os.path.abspath(sys.argv[0])))

global EchoInstance

def openeditor(dt):
    #subprocess.Popen([os.path.join(mypath, 'MapEditor.exe')])
    subprocess.Popen([sys.executable, os.path.join(mypath, 'MapEditor.py')])
Clock.schedule_once(openeditor, 5)

#from kivy.support import install_twisted_reactor
def install_twisted_reactor(**kwargs):
    '''Installs a threaded twisted reactor, which will schedule one
    reactor iteration before the next frame only when twisted needs
    to do some work.

    any arguments or keyword arguments passed to this function will be
    passed on the the threadedselect reactors interleave function, these
    are the arguments one would usually pass to twisted's reactor.startRunning

    Unlike the default twisted reactor, the installed reactor will not handle
    any signals unnless you set the 'installSignalHandlers' keyword argument
    to 1 explicitly.  This is done to allow kivy to handle teh signals as
    usual, unless you specifically want the twisted reactor to handle the
    signals (e.g. SIGINT).'''
    import twisted

    # prevent installing more than once
    if hasattr(twisted, '_kivy_twisted_reactor_installed'):
        return
    twisted._kivy_twisted_reactor_installed = True

    # dont let twisted handle signals, unless specifically requested
    kwargs.setdefault('installSignalHandlers', 0)

    # install threaded-select reactor, to use with own event loop
    from twisted.internet import _threadedselect
    _threadedselect.install()

    # now we can import twisted reactor as usual
    from twisted.internet import reactor
    from collections import deque
    from kivy.base import EventLoop
    from kivy.logger import Logger
    from kivy.clock import Clock

    # will hold callbacks to twisted callbacks
    q = deque()

    # twisted will call the wake function when it needsto do work
    def reactor_wake(twisted_loop_next):
        Logger.trace("Support: twisted wakeup call to schedule task")
        q.append(twisted_loop_next)

    # called every frame, to process the reactors work in main thread
    def reactor_work(*args):
        Logger.trace("Support: processing twisted task queue")
        while len(q):
            q.popleft()()

    # start the reactor, by telling twisted how to wake, and process
    def reactor_start(*args):
        Logger.info("Support: Starting twisted reactor")
        reactor.interleave(reactor_wake, **kwargs)
        Clock.schedule_interval(reactor_work, 0)

    # make sure twisted reactor is shutdown if eventloop exists
    def reactor_stop(*args):
        '''will shutdown the twisted reactor main loop
        '''
        if reactor.threadpool:
            Logger.info("Support: Stooping twisted threads")
            reactor.threadpool.stop()
        Logger.info("Support: Shutting down twisted reactor")
        reactor._mainLoopShutdown()

    # start and stop teh reactor along with kivy EventLoop
    EventLoop.bind(on_start=reactor_start)
    EventLoop.bind(on_stop=reactor_stop)
install_twisted_reactor()

from twisted.internet import reactor
from twisted.internet import protocol

class EchoProtocol(protocol.Protocol):
    def dataReceived(self, data):
        response = self.factory.app.handle_message(data)
        if response:
            self.transport.write(response)
    def connectionMade(self):
        global EchoInstance
        self.factory.app.registerNewConnection(self)

class EchoFactory(protocol.Factory):
    protocol = EchoProtocol
    def __init__(self, app):
        self.app = app
        Logger.info('Connected.')
    #def buildProtocol(addr):
    #    self.protocol = EchoProtocol
    #    return self.protocol
    def startedConnecting(self, connector):
        Logger.info('Started to connect.')
    def clientConnectionLost(self, connector, reason):
        Logger.info('Lost connection.  Reason:', reason)
    def clientConnectionFailed(self, connector, reason):
        Logger.info('Connection failed. Reason:', reason)

#class EchoClient(protocol.Protocol):
#    def connectionMade(self):
#        self.factory.app.on_connection(self.transport)
#        #self.factory.app.on_connection(self.transport)
#
#    def dataReceived(self, data):
#        response = self.factory.app.handle_message(data)
#
#    #def connectionMade(self):
#    #    global EchoInstance
#    #    self.factory.app.registerNewConnection(self)
#
#class EchoFactory(protocol.ClientFactory):
#    protocol = EchoClient
#    def __init__(self, app):
#        self.app = app
#
#    def clientConnectionLost(self, conn, reason):
#        self.app.print_message("connection lost")
#
#    def clientConnectionFailed(self, conn, reason):
#        self.app.print_message("connection failed")

#EchoInstance.transport.write('hello')

#from mastermind_import import *
#
#class ServerChat(MastermindServerTCP):
#    def __init__(self):
#        MastermindServerTCP.__init__(self, 0.5,0.5,10) #server refresh, connections' refresh, connection timeout
#
#
#    def add_message(self, msg):
#        pass
#
#    def callback_connect          (self                                          ):
#        #Something could go here
#        Logger.info('title:Connected')
#        return super(ServerChat,self).callback_connect()
#    def callback_disconnect       (self                                          ):
#        #Something could go here
#        Logger.info('title:Disconnected')
#        return super(ServerChat,self).callback_disconnect()
#    def callback_connect_client   (self, connection_object                       ):
#        #Something could go here
#        Logger.info('title:Client connected')
#        return super(ServerChat,self).callback_connect_client(connection_object)
#    def callback_disconnect_client(self, connection_object                       ):
#        Logger.info('title:Disconnected all clients')
#        #Something could go here
#        return super(ServerChat,self).callback_disconnect_client(connection_object)
#
#    def callback_client_receive   (self, connection_object                       ):
#        #Something could go here
#        Logger.info('title:Just receives some data')
#        return super(ServerChat,self).callback_client_receive(connection_object)
#    def callback_client_handle    (self, connection_object, data                 ):
#        Logger.info('title:Received data')
#        cmd = data
#        if cmd == "nuclear":
#            Logger.info('title:nuclear')
#        #self.callback_client_send(connection_object, self.chat)
#    def callback_client_send      (self, connection_object, data,compression=9):
#        #Something could go here
#        return super(ServerChat,self).callback_client_send(connection_object, data,compression=9)
#server = ServerChat()
#server.connect('127.0.0.1', 50007)
#server.accepting_allow()

class MenuView(AnchorLayout):
    def my_callback(self, dt):
        AppInstance.stop()
    def HandleInput(self, cmd):
        if cmd == 'Save map':
            EchoInstance.transport.write('save')
        if cmd == 'Test map in offline mode':
            EchoInstance.transport.write('quit')
            os.system('python ' + os.path.join(mypath, 'MapTest.py'))
            AppInstance.stop()
        if cmd == 'Quit editor':
            EchoInstance.transport.write('quit')
            Clock.schedule_once(self.my_callback, 2)
            #AppInstance.stop()

Factory.register('MenuView', MenuView)

class PowerupView(AnchorLayout):
    current_checkbox = StringProperty()
    heal = ObjectProperty()
    speed = ObjectProperty()
    shield = ObjectProperty()

    def on_current_checkbox(self, instance, value):
        global EchoInstance
        if value == 'Heal':
            EchoInstance.transport.write('heal')
        if value == 'Speed':
            EchoInstance.transport.write('speed')
        if value == 'Shield':
            EchoInstance.transport.write('shield')

Factory.register('PowerupView', PowerupView)

class SpawnView(AnchorLayout):
    biohazard = ObjectProperty()
    nuclear = ObjectProperty()
    current_checkbox = StringProperty()

    def on_current_checkbox(self, instance, value):
        global EchoInstance
        #print instance, value
        #app.protocol.transport.write('lol')
        if value == 'Bio-hazard':
            EchoInstance.transport.write('biohazard')
            #pass
        if value == 'Nuclear':
            EchoInstance.transport.write('nuclear')
            #EchoInstance.send_message('nuclear')
            #pass

    def __init__(self, **kwargs):
        super(SpawnView, self).__init__(**kwargs)
        #self.biohazard.bind(active=self.on_checkbox_active('biohazard'))
        #self.nuclear.bind(active=self.on_checkbox_active('nuclear'))

Factory.register('SpawnView', SpawnView)

class MoveView(FloatLayout):
    speed = ObjectProperty()
    length = ObjectProperty()
    offset = ObjectProperty()
    speedcounter = ObjectProperty()
    lengthcounter = ObjectProperty()
    offsetcounter = ObjectProperty()

    xselect = ObjectProperty()
    yselect = ObjectProperty()

    speed_x = NumericProperty(55)
    speed_y = NumericProperty(55)
    length_x = NumericProperty(55)
    length_y = NumericProperty(55)
    offset_x = NumericProperty(50)
    offset_y = NumericProperty(50)

    def __init__(self, lx, ly, sx, sy, ox, oy, **kwargs):
        super(MoveView, self).__init__(**kwargs)
        self.xselect.state = 'down'
        self.speed_x = self.speed.value * 0.002 -0.1
        self.length_x = self.length.value * 2 -100
        self.offset_x = (self.offset.value - 50) * 6.283/100
        self.speed_y = self.speed.value * 0.002 -0.1
        self.length_y = self.length.value * 2 -100
        self.offset_y = (self.offset.value - 50) * 6.283/100

        self.speed_x = sx
        self.length_x = lx
        self.offset_x = ox
        self.speed_y = sy
        self.length_y = ly
        self.offset_y = oy

        self.updatecounters()
        self.updatex()

    def updatecounters(self):
        if self.xselect.state == 'down':
            self.speedcounter.text = str(self.speed_x)
            self.lengthcounter.text = str(self.length_x)
            self.offsetcounter.text = str(self.offset_x)

        else:
            self.speedcounter.text = str(self.speed_y)
            self.lengthcounter.text = str(self.length_y)
            self.offsetcounter.text = str(self.offset_y)

    def send_stats(self):
        EchoInstance.transport.write('i'+pickle.dumps([self.length_x, self.length_y, self.speed_x, self.speed_y, self.offset_x, self.offset_y]))

    def updatex(self):
        self.updatecounters()
        self.speed.value = -500*(-self.speed_x-0.1)
        self.length.value = (self.length_x + 100) / 2
        self.offset.value = (-self.offset_x-3.1415) * -15.916
        self.updatecounters()

    def updatey(self):
        self.updatecounters()
        self.speed.value =  -500*(-self.speed_y-0.1)
        self.length.value = (self.length_y + 100) / 2
        self.offset.value = (-self.offset_y-3.1415) * -15.916
        self.updatecounters()

    def updatenumbers(self):
        if self.xselect.state == 'down':
            self.speed_x = self.speed.value * 0.002 -0.1
            self.length_x = self.length.value * 2 -100
            self.offset_x = (self.offset.value - 50) * 6.283/100
            self.updatecounters()

        else:
            self.speed_y = self.speed.value * 0.002 -0.1
            self.length_y = self.length.value * 2 -100
            self.offset_y = (self.offset.value - 50) * 6.283/100
            self.updatecounters()

        self.send_stats()


    


Factory.register('MoveView', MoveView)

class Controller(FloatLayout):
    container = ObjectProperty()
    menu = ObjectProperty()

    def __init__(self, **kwargs):
        super(Controller, self).__init__(**kwargs)
        #self.container.add_widget(SpawnView())
        self.menu.add_widget(MenuView())

class MapEditorApp(App):
    icon = 'ICO.ico'
    title = 'Map editor controller'
    connection = None

    def registerNewConnection(self, connection):
        global EchoInstance
        EchoInstance = connection

    def build(self):
        self.controller = Controller()
        #self.connect_to_server()
        self.controller.container.clear_widgets()
        #self.controller.container.add_widget(MoveView())
        reactor.listenTCP(50007, EchoFactory(self))
        return self.controller

    #def on_stop(self):
    #    global server
    #    server.disconnect_clients()
    #    server.accepting_disallow()
    #    server.disconnect()

    def handle_message(self, msg):
        Logger.info('title: MSG received')
        if msg[0] == '0':
            self.controller.container.clear_widgets()
        if msg[0] == '1':
            self.controller.container.clear_widgets()
        if msg[0] == '2':
            self.controller.container.clear_widgets()
            numbers = pickle.loads(msg[1:])
            moveviewinstance = MoveView(numbers[0], numbers[1], numbers[2], numbers[3], numbers[4], numbers[5])
            self.controller.container.add_widget(moveviewinstance)
        if msg[0] == '3':
            self.controller.container.clear_widgets()
            spawnviewinstance = SpawnView()
            self.controller.container.add_widget(spawnviewinstance)
            if msg[1] == '0':
                spawnviewinstance.biohazard.active = True
                spawnviewinstance.nuclear.active = False
            if msg[1] == '1':
                spawnviewinstance.biohazard.active = False
                spawnviewinstance.nuclear.active = True
        if msg[0] == '4':
            self.controller.container.clear_widgets()
            powerupinstance = PowerupView()
            self.controller.container.add_widget(powerupinstance)
            if msg[1] == '0':
                #powerupinstance.current_checkbox = 'Heal'
                #powerupinstance.heal.state = 'down'
                powerupinstance.heal.active = True
                powerupinstance.speed.active = False
                powerupinstance.shield.active = False
            if msg[1] == '1':
                #powerupinstance.current_checkbox = 'Speed'
                powerupinstance.heal.active = False
                powerupinstance.speed.active = True
                powerupinstance.shield.active = False
            if msg[1] == '2':
                #powerupinstance.current_checkbox = 'Shield'
                #powerupinstance.shield.state = 'down'
                powerupinstance.heal.active = False
                powerupinstance.speed.active = False
                powerupinstance.shield.active = True
        return msg

    #def connect_to_server(self):
    #    reactor.connectTCP('127.0.0.1', 50007, EchoFactory(self))

    #def on_connection(self, connection):
    #    Logger.info('title: Connected successfuly')
    #    self.connection = connection

    #def send_message(self, msg, *args):
    #    #Logger.info('title: Sent MSG')
    #    self.connection.write(str(msg))
    #    Logger.info('title: Sent MSG')

if __name__ == '__main__':
    global EchoInstance
    EchoInstance = MapEditorApp()
    AppInstance = MapEditorApp()
    AppInstance.run()
