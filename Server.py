#!/usr/bin/env python2.7
# Last Hazard on the Moon (A 2D Online Myltiplayer Platformer Shooter for Android --- yeah, it's that cool)
# By Mark Beiline ohmnivore.elementfx.com
# Created with PyGame

from pygame.locals import *
import legume
import pygame._view
import pygame, pygame.mixer, os, sys # copy
import random
import math, pickle
import euclid     #from https://code.google.com/p/pyeuclid/
import traceback
import threading
from os import walk
import zlib, base64
parentdir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0,parentdir)
import urllib2, socket
import pymunk
from pymunk.vec2d import Vec2d
from pymunk import Vec2d
import json
from configobj import ConfigObj
import time
import cmd2 as cmd
import datetime
import atexit
import os
import requests

def cleanexit(lol):
    running = False
    server.disconnect_all()
    t1._Thread__stop()
    server_cmd._Thread__stop()
    data = {'cmd': '-'}
    if ms_public == True:
        r = requests.post(config['Masterserver']['ms_ip'], data)

def cleanexit2():
    running = False
    server.disconnect_all()
    t1._Thread__stop()
    server_cmd._Thread__stop()
    data = {'cmd': '-'}
    if ms_public == True:
        r = requests.post(config['Masterserver']['ms_ip'], data)

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
config = ConfigObj(os.path.join(mypath,'ServerSettings.cfg'))

#Windows-specific
if config['OS'] == 'Windows':
    import win32api
    win32api.SetConsoleCtrlHandler(cleanexit, True)

#Linux-specific
if config['OS'] == 'Linux':
    import signal
    signal.signal(signal.SIGTERM, cleanexit)

atexit.register(cleanexit2)

global status
global player
global mapmenu
global options

def to_pygame(p):
    return int(p[0]),600 - int(p[1])

def from_pygame(p):
    return to_pygame(p)

class FetchUrls(threading.Thread):
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
        while self.connection:
            self.connection.update()
            time.sleep(0.0001)

class CLI(cmd.Cmd):
    """Command line interface for FRENZY server."""

    status = False
    player = False
    mapmenu = False
    options = False

    prompt = ''
    
    intro = "\n*Welcome to the frenzy server command line interface*\nType menu or help to get started\nUse menu, status, player, map, and options to get around\nCommands called outside of their menu's scope will not be executed\n"

    def save_config(self):
        cfg = ConfigObj(os.path.join(mypath,'ServerSettingsDefault.cfg'))
        cfg.merge(config)
        cfg.write(open(os.path.join(mypath,'ServerSettings.cfg'), 'wb'))

    def do_menu(self, line):
        "Returns to main menu"
        global web, connect, custom, mapping, credit, setting
        print '\nMain menu active.\nAvailable menus: status, player, map, options\n'
        status = False
        player = False
        mapmenu = False
        options = False

    def do_status(self, line):
        "Opens up the server status menu"
        global status
        print '\nStatus menu active.\nAvailable commands: ip, stats, fps \n'
        status = True

    def do_player(self, line):
        "Opens up the player management menu"
        global player
        print '\nPlayer menu active.\nAvailable commands: player, kick, send \n'
        player = True

    def do_map(self, line):
        "Opens up the map rotation management menu"
        global mapmenu
        print '\nMap menu active.\nAvailable commands: rotation, set, update_maps\n'
        mapmenu = True

    def do_options(self, line):
        "Opens up the map rotation management menu"
        global options
        print '\nOptions menu active.\nAvailable commands: \n'
        options = True

    #def do_EOF(self, line):
    #    "Closes the FRENZY command line interface session"
    #    global running
    #    running = False
    #    server.disconnect_all()
    #    #raise KeyboardInterrupt
    #    t1._Thread__stop()
    #    server_cmd._Thread__stop()
    #    raise KeyboardInterrupt
    #    
    #    #return True
    ##    #raise KeyboardInterrupt

    def do_shell(self, line):
        "Runs a shell command"
        print "running shell command:", line
        output = os.popen(line).read()
        print output
        self.last_output = output

    def do_ip(self, line):
        "Displays internal, and public IP"
        print "\nPublic IP: " + pub_ip
        print "Internal IP: " + int_ip
        print "Bound to: " + config['Connection']['bind_IP']
        print "Port: 6385\n"

    def do_stats(self, line):
        "Displays current server stats"
        print '\nServer name: ' + ServerName
        print 'Map: ' + MapName
        print 'Game mode: ' + 'DM'
        print 'Max players: ' + str(MaxPlayers)
        print 'Current players: ' + str(CurrentPlayers) + '\n'

    def do_fps(self, line):
        "Displays the server's average FPS for two seconds."
        y = 0
        sumfps = 0
        while y < 20:
            time.sleep(0.1)
            sumfps += int(FPSCLOCK.get_fps())
            y += 1
        averagefps = sumfps / 20
        print averagefps

    def do_players(self, line):
        "Displays all connected players and their attributes"
        print "\nID|Name|Join hour:minute|Score|Kills/Deaths"
        for player in PlayerList:
            print player.id, '|', player.name,'|', player.jointime.hour, ":", player.jointime.minute,'|', player.score,'|', player.kills, "/", player.deaths

    def do_kick(self, line):
        "Kicks the player with the specified ID. Execute 'players' to get a list of all players and their IDs."
        try:
            theplayer = ''
            for player in PlayerList:
                if player.id == int(line):
                    theplayer = player
            if theplayer == '':
                print "Did not find any connected player with the specified ID."
            for key in IPRegistry.keys():
                if IPRegistry[key] == theplayer:
                    global space
                    try:
                        if IPRegistry[key] in PlayerList:
                            Disco.id.value = IPRegistry[key].id
                            IPRegistry[key].disconnecting = True
                            print 'Kicked player: ' + IPRegistry[key].name
                            playernamelist.remove(IPRegistry[key].name)
                            PlayerList.remove(IPRegistry[key])
                            SenderList.remove(server.get_peer_by_address(key))
                            space.remove(IPRegistry[key].body, IPRegistry[key].shape)
                
                            for x in SenderList:
                                x.send_reliable_message(Disco)
                            del IPRegistry[key]
                            server.disconnect(key)
                            data = {'cmd': '-p'}
                            if ms_public == True:
                                r = requests.post(config['Masterserver']['ms_ip'], data)
                    except:
                        pass
        except:
            print "Did not find any connected player with the specified ID."

    def do_send(self, line):
        "Sends a message to the specified player (ID) or pass 0 as ID to send the message to all connected players. Example syntax (will send 'example message' to all players): send 0 example message"
        try:
            Chatmessage.id.value = 0
            Chatmessage.msg.value = line[0:]
            Chatmessage.placeholder.value = 100
            if line[0] == '0':
                server.send_reliable_message_to_all(Chatmessage)
            else:
                theplayer = ''
                for player in PlayerList:
                    if player.id == int(line[0]):
                        theplayer = player
                if theplayer == '':
                    print "\nDid not find any connected player with the specified ID."
                for key in IPRegistry.keys():
                    if IPRegistry[key].id == theplayer.id:
                        server.get_peer_by_address(key).send_reliable_message(Chatmessage)
        except:
            print "Could not send to the specified player. Check the ID.\n"

    def do_rotation(self, line):
        "Shows current map rotation and indicates the current map."
        print '\n'
        global MapName
        for mapnamez in ServerRotation:
            x = mapnamez[:-4]
            if x == MapName:
                print '> ' + MapName
            else:
                print x

    def do_update_maps(self, line):
        "Updates the map rotation. Use this if you modify the 'Server rotation' directory while the server is running for changes to take effect."
        ServerRotation = []
        for (dirpath, dirnames, filenames) in walk(os.path.join(mypath, 'Server rotation')):
            ServerRotation.extend(filenames)
            break

    def do_set(self, line):
        "Changes the current map to the specified one."
        #try:
        global MapName
        global my_map, ServerRotation, PlayerList, space, posix
        found = False
        posix = 0
        for x in ServerRotation:
            if line == x[:-4]:
                MapName = line
                found = True
                #print pos
                break
            posix += 1
        if found == False:
            print "\nCould not find the specified map in the 'Server rotation' directory. Make sure you call 'update_maps' if you have modified its contents.\n"
        if found == True:
            #with lock:
                #print posix
                #Send new map
            ServerRotation = []
            for (dirpath, dirnames, filenames) in walk(os.path.join(mypath, 'Server rotation')):
                ServerRotation.extend(filenames)
                break
            my_map.spawns = []
            my_map.spawnlist = []
            space = pymunk.Space()
            space.gravity = (0.0, -700.0)
            space.collision_slop = 0.0001
            space.collision_bias = pow(1.0-0.1, 120.0)
            for platform in my_map.platforms:
                space.remove(platform.shape)
            for platform in my_map.movingplatforms:
                space.remove(platform.shape)
            for platform in my_map.poweruplist:
                space.remove(platform.shape)
            MapName = str(ServerRotation[0][0:-4])
            MapInfos = MapInfo()
            mapopened = open(os.path.join(mypath, 'Server rotation', ServerRotation[0]), 'r').read()
            mapstring = base64.b64encode(zlib.compress(json.dumps(pickle.loads(mapopened)),9))
            my_mapz = Map(str(ServerRotation[0][0:-4]), mapopened)
            my_map = my_mapz
            numberchunks = len(mapstring)/((len(mapstring)/1200) + 1)
            chunk = 0
            chunkedmapstring = [''.join(x) for x in zip(*[list(mapstring[z::numberchunks]) for z in range(numberchunks)])]

            for player in PlayerList:
                player.deaths = 0
                player.kills = 0
                player.score = 0
                space.remove(player.body, player.shape)
                spawnpoint = my_map.spawns[random.randint(0, len(my_map.spawns)-1)]
                player.body = pymunk.Body(1, pymunk.inf)
                player.body.position = from_pygame((spawnpoint.position_x+65, spawnpoint.position_y+65))
                player.shape = pymunk.Poly(player.body, [(0,40), (40,40), (40,0), (0,0)])
                player.shape.friction = 0.1
                player.shape.elasticity = 0.0
                space.add(player.body, player.shape)

            while chunk + 1 <= (len(mapstring)/1200) + 1:
                MapInfos.chunks.value = (len(mapstring)/1200) + 1
                MapInfos.chunk.value = chunk
                MapInfos.map.value = chunkedmapstring[chunk]
                MapInfos.name.value = str(ServerRotation[0])
                server.send_reliable_message_to_all(MapInfos)
                chunk += 1
            chunk = 0

            for platform in my_map.activepowerups:
                PwupMsg.id.value = my_map.powerups.index(platform)
                PwupMsg.active.value = True
                server.send_reliable_message_to_all(PwupMsg)
        #except:
        #    print "\nCould not find the specified map in the 'Server rotation' directory. Make sure you call 'update_maps' if you have modified its contents.\n"

class ServerCLI(threading.Thread):
    """
    Thread checking URLs.
    """

    def __init__(self):
        """
        Constructor.

        @param urls list of urls to check
        @param output file to write urls output
        """
        threading.Thread.__init__(self)
    
    def run(self):
        """
        Thread run method. Check URLs one by one.
        """
        if len(sys.argv) > 1:
            CLI().onecmd(' '.join(sys.argv[1:]))
        else:
            CLI().cmdloop()

server_cmd = ServerCLI()
server_cmd.start()

global FPSCLOCK, running, mx, my, dtime, dtime_ms
global RocketList, rocketdist, sx, sy
global mapx, mapy, lolx, loly
global reloadclock, dfps
mapstring = ''
my_map = None
reloadclock = 0
lololol = 0
RocketList = []
reloaded = True
running = True
groups = 1

FPS = 50  # frames per second to update the screen
WINWIDTH = 800  # width of the program's window, in pixels
WINHEIGHT = 600  # height in pixels

#Colors
white = 255,255,255
red = 151, 51, 51
green = 112, 145, 28
yellow = 222, 200, 29
blue = 51, 102, 153
black = 0, 0, 0

pygame.init()
pygame.font.init()
FPSCLOCK = pygame.time.Clock()

# Setting of the system icon
icon=pygame.image.load(os.path.join(mypath, 'Images', 'ICO.ico'))
#icon=pygame.image.load('ICO.ico')
pygame.display.set_icon(icon)

# Setting of the caption and global font
pygame.display.set_caption('Last Hazard on the Moon')
BRUSH = pygame.font.Font(os.path.join(mypath, 'Fonts', 'ElectricCity.TTF'), 18)

# The variable that keeps the main loop running
running = True

# A variable to determine if the user is moving the player
moving = False

# Set key repeat to repeatable
pygame.key.set_repeat(1, 8)

posix = 0
lock = threading.Lock()

space = pymunk.Space()
space.gravity = (0.0, -700.0)
space.collision_slop = 0.0001
space.collision_bias = pow(1.0-0.1, 120.0)
#space.add_collision_handler()

class Platform:
    def __init__(self, position_x, position_y, variety, mode):
        self.position_x = position_x
        self.position_y = position_y
        self.type = variety
        self.mode = mode
        self.bound = None
        self.body = None
        self.shape = None
        self.timer = 0
        self.parent = None
        self.pwup = mode

# The map class is for reading and displaying a map
class Map:
    def __init__(self, mapname, maptext):
        global space

        self.mapname = str(mapname)
        self.lowest_y = 0

        self.powerups = []
        self.platforms = []
        self.spawns = []
        self.movingplatforms = []
        self.PowerTimes = []
        self.spawnlist = []
        self.spawnlist = []
        self.poweruplist = []
        self.activepowerups = []
        self.deletedpowerups = []
        for x in pickle.loads(maptext):
            if self.lowest_y < x[1]:
                self.lowest_y = x[1] + 300
            platform = Platform(x[0], x[1], x[2], x[3])
            platform.mode = x[3]
            if x[2] == 0:
                platform.bound = Rect(x[0], x[1], 168, 22)
                platform.body = pymunk.Body()
                platform.body.position = from_pygame(Vec2d(platform.position_x, platform.position_y))
                xp, yp = platform.bound.topleft
                width = platform.bound.width
                height = platform.bound.height
                platform.shape = pymunk.Poly(space.static_body, [from_pygame(Vec2d(xp,yp)), from_pygame(Vec2d(xp+width,yp)), from_pygame(Vec2d(xp+width,yp+height)), from_pygame(Vec2d(xp,yp+height))])
                platform.shape.friction = 2.4
                space.add(platform.shape)
                self.platforms.append(platform)

            if x[2] == 1:
                platform.bound = Rect(x[0], x[1], 168, 168)
                platform.body = pymunk.Body()
                platform.body.position = from_pygame(Vec2d(platform.position_x, platform.position_y))
                xp, yp = platform.bound.topleft
                width = platform.bound.width
                height = platform.bound.height
                platform.shape = pymunk.Poly(space.static_body, [from_pygame(Vec2d(xp,yp)), from_pygame(Vec2d(xp+width,yp)), from_pygame(Vec2d(xp+width,yp+height)), from_pygame(Vec2d(xp,yp+height))])
                platform.shape.friction = 2.4
                space.add(platform.shape)
                self.platforms.append(platform)
            if x[2] == 2:
                platform.initposx = platform.position_x
                platform.initposy = platform.position_y
                platform.lx = x[4]
                platform.ly = x[5]
                platform.sx = x[6]
                platform.sy = x[7]
                platform.ox = x[8]
                platform.oy = x[9]
                platform.xxx = 0
                platform.yyy = 0
                platform.bound = Rect(x[0], x[1], 168, 22)
                platform.body = pymunk.Body(100000,pymunk.inf)
                platform.body.position = from_pygame(Vec2d(platform.position_x, platform.position_y))
                xp, yp = platform.bound.topleft
                width = platform.bound.width
                height = platform.bound.height
                platform.shape = pymunk.Poly(space.static_body, [from_pygame(Vec2d(xp,yp)), from_pygame(Vec2d(xp+width,yp)), from_pygame(Vec2d(xp+width,yp+height)), from_pygame(Vec2d(xp,yp+height))])
                platform.shape.friction = 2.4
                space.add(platform.shape)
                self.platforms.append(platform)
                self.movingplatforms.append(platform)
                platform.body.apply_force(Vec2d(0.0, 700.0))
            if x[2] == 3:
                platform.bound = Rect(x[0], x[1], 168, 168)
                platform.body = pymunk.Body()
                platform.body.position = from_pygame(Vec2d(platform.position_x, platform.position_y))
                self.spawns.append(platform)
                self.spawnlist.append(platform.shape)
            if x[2] == 4:
                platform.bound = Rect(x[0] + 63, x[1] + 63, 42, 42)
                platform.body = pymunk.Body()
                platform.body.position = from_pygame(Vec2d(platform.position_x, platform.position_y))
                xp, yp = platform.bound.topleft
                width = platform.bound.width
                height = platform.bound.height
                platform.shape = pymunk.Poly(space.static_body, [from_pygame(Vec2d(xp,yp)), from_pygame(Vec2d(xp+width,yp)), from_pygame(Vec2d(xp+width,yp+height)), from_pygame(Vec2d(xp,yp+height))])
                platform.shape.friction = 0.0
                platform.shape.sensor = True
                space.add(platform.shape)
                if x[3] == 0:
                    platform.pwup = 0
                if x[3] == 1:
                    platform.pwup = 1
                if x[3] == 2:
                    platform.pwup = 2
                self.powerups.append(platform)
                self.activepowerups.append(platform)
                self.poweruplist.append(platform.shape)

# The player class: represents the controllable character on screen
class Playerz:

    def __init__(self, position, colour, name , health , velocity):
        global space, groups
        self.jointime = datetime.datetime.now()
        self.score = 0
        self.kills = 0
        self.deaths = 0
        self.lastshot = None
        self.lastshotid = 0
        self.mx = False
        self.timeout = 0
        self.disconnecting = False
        self.id = None
        self.right = False
        self.left = False
        #self.PlayerInfo = pickle.load(open(os.path.join(mypath, 'TXT Files', 'PlayerInfo.txt'), 'r'))
        self.colour = colour
        self.name = name
        self.reloadspeed = random.randint(0, 15)
        self.weaponvelocity = random.randint(0, 15 - self.reloadspeed)
        self.damage = random.randint(0, 15 - self.reloadspeed - self.weaponvelocity)
        self.cacheddamage = 700 + self.damage * 25
        self.cachedvelocity = 15 + self.weaponvelocity
        self.cachedreloadspeed = 1500 - self.reloadspeed * 50

        self.armor = random.randint(0, 15)
        self.speed = random.randint(0, 15 - self.armor)
        self.energy = random.randint(0, 15 - self.armor - self.speed)
        self.cachedarmor = 1 + self.armor * 0.03
        self.cachedspeed = 1 + self.speed * 0.1
        self.cachedenergy = 0.1 + self.energy * 0.1

        if self.armor > 5:
            self.displayarmor = True
        else:
            self.displayarmor = False
        if self.speed > 5:
            self.displayshoes = True
        else:
            self.displayshoes = False
        if self.energy > 5:
            self.displaypack = True
        else:
            self.displaypack = False

        self.shoot = False
        self.abilitystatus = False
        self.a = 1
        self.position = position
        self.health = health
        self.velocity = velocity
        self.rect = pygame.Rect(379 -2, 279 -2, 46, 46)
        self.armor = 1
        self.shielded = False
        self.speedup = 1
        self.speeded = False
        self.inAir = False
        self.gravity = 0.04
        self.isOn1 = False
        self.body = pymunk.Body(1, pymunk.inf)
        self.body.position = from_pygame(self.position)
        self.shape = pymunk.Poly(self.body, [(0,40), (40,40), (40,0), (0,0)])
        self.shape.friction = 0.1
        self.shape.elasticity = 0.0
        self.shape.group = groups
        groups += 1
        #self.shape.group = 1
        space.add(self.body, self.shape)
        self.timer = 0
        self.cachedname = 0

    def checkIfValid(self):
        if self.reloadspeed + self.weaponvelocity + self.damage > 15:
            self.reloadspeed, self.weaponvelocity, self.damage = 0
        if self.armor + self.speed + self.energy > 15:
            self.armor, self.speed, self.energy = 0

    def move(self):
        global killfeed
        #print self.body.position
        if len(space.shape_query(self.shape)) > 0: #or space.segment_query_first(self.oldpos, self.body.position) != None
            for i in space.shape_query(self.shape):
                for platform in my_map.activepowerups:
                    if platform.shape == i:
                        if platform.pwup == 0:
                            if self.health < 100:
                                if self.health <= 75:
                                    self.health += 25
                                else:
                                    self.health = 100
                                platform.parent = self
                                my_map.activepowerups.remove(platform)
                                my_map.deletedpowerups.append(platform)
                                PwupMsg.id.value = my_map.powerups.index(platform)
                                PwupMsg.active.value = False
                                server.send_reliable_message_to_all(PwupMsg)
                        if platform.pwup == 1:
                            self.cachedspeed += 1
                            platform.parent = self
                            my_map.activepowerups.remove(platform)
                            my_map.deletedpowerups.append(platform)
                            PwupMsg.id.value = my_map.powerups.index(platform)
                            PwupMsg.active.value = False
                            server.send_reliable_message_to_all(PwupMsg)
                        if platform.pwup == 2:
                            self.cachedarmor += 0.25
                            platform.parent = self
                            my_map.activepowerups.remove(platform)
                            my_map.deletedpowerups.append(platform)
                            PwupMsg.id.value = my_map.powerups.index(platform)
                            PwupMsg.active.value = False
                            server.send_reliable_message_to_all(PwupMsg)
                for player in PlayerList:
                    if player != self:
                        if player.shape == i:
                            if player.position.y < self.position.y:
                                self.kills += 1
                                self.score += 100
                                player.deaths += 1
                                player.DieNow()
                                killfeed.append((self.id, 'SQUISHED!', self.id, random.randint(0, 255)))

        if self.right == True:
            self.body.velocity += (self.cachedspeed*30,0)

        if self.left == True:
            self.body.velocity -= (self.cachedspeed*30,0)

        if self.body.velocity.y > 700:
            self.body.velocity.y = 700
        if self.body.velocity.x > 600+ self.cachedspeed * 30:
            self.body.velocity.x = 600 + self.cachedspeed * 30
        if self.body.velocity.x < -600 - self.cachedspeed * 30:
            self.body.velocity.x = -600 - self.cachedspeed * 30
        if self.body.position.y < -my_map.lowest_y+600 - 700:
            killfeed.append((self.id, 'IS NO MORE!', self.id, random.randint(0, 255)))
            self.DieNow()
            self.inAir = False
        self.body.velocity.x *= 0.95

        global dtime_ms
        self.timeout += dtime_ms
        rx = int(379)
        ry = int(279)
        if self.health > 100:
            self.health = 100
        if self.health <= 0:
            self.DieNow()
        self.timer += dtime_ms
        if self.timer > self.cachedreloadspeed - 1:
            self.timer = self.cachedreloadspeed


    def DieNow(self):
        self.deaths += 1
        self.health = 100
        spawnpoint = my_map.spawns[random.randint(0, len(my_map.spawns)-1)]
        self.body.position = Vec2d(spawnpoint.position_x+65, spawnpoint.position_y+335)
        self.body.velocity = (0,0)
        self.armor -= 0.04
        self.shielded = False
        self.speeded = False

# The rocket class: represents the projectiles
class Rocket:
    def __init__(self, parent, a, mx, start_pos):
        self.ExploBlueCopy = 0
        mass = 1
        radius = 18
        inertia = pymunk.moment_for_circle(mass, 0, radius)
        self.body = pymunk.Body(mass, inertia)
        self.body.position = start_pos + (5,18)
        self.oldpos = self.body.position
        self.shape = pymunk.Circle(self.body, 9)
        self.shape.group = parent.shape.group
        space.add(self.body, self.shape)
        self.parent = parent
        self.parent.timer = 0
        self.a = a
        self.mx = mx
        if mx == True:
            self.angle = math.atan(self.a)
            #print self.angle
            self.body.lol = Vec2d(parent.cachedvelocity, 0)
            self.impulse = Vec2d((self.body.lol.rotated(self.angle)*20)+(parent.body.velocity/2))
            self.body.apply_impulse(self.impulse)
        else:
            self.angle = math.atan(self.a)
            #print self.angle
            self.body.lol = Vec2d(-parent.cachedvelocity, 0)
            self.impulse = Vec2d((self.body.lol.rotated(self.angle)*20)+(parent.body.velocity/2))
            self.body.apply_impulse(self.impulse)
        self.shape.sensor = True
        RocketList.append(self)

    def DisplayRocket(self):
        global killfeed
        self.body.apply_force(self.body.mass*space.gravity*-1)
        if space.segment_query_first(self.oldpos, self.body.position) != None or len(space.shape_query(self.shape)) > 0:
            for i in space.shape_query(self.shape):
                if i not in my_map.spawnlist and i not in my_map.poweruplist:
                    for player in PlayerList:
                        diff = player.body.position - self.body.position + Vec2d(5,15)
                        length = diff.length
                        direc = diff.normalized()
                        lol =( 700 - length*9) * (self.parent.damage + 15)/75 * 4
                        if lol < 0:
                            lol = 0
                        direc *= lol
                        player.body.apply_impulse(direc)
                        if player != self.parent:
                            player.health -= direc.length / 7 * player.cachedarmor
                            if player.health <= 0:
                                self.parent.kills += 1
                                killfeed.append((self.parent.id, random.choice(expletiveslist), player.id, random.randint(0, 255)))
                            self.parent.score += direc.length / 7
                        if self in RocketList:
                            RocketList.remove(self)
        self.oldpos = self.body.position.int_tuple

class ArrowStatusMsg(legume.messages.BaseMessage):
    MessageTypeID = legume.messages.BASE_MESSAGETYPEID_USER+2
    MessageValues ={
    'arrows': 'string 4',
    'gunorientation' : 'float',
    'mx' : 'bool',
    'ability' : 'bool'
    }

class PwupStatus(legume.messages.BaseMessage):
    MessageTypeID = legume.messages.BASE_MESSAGETYPEID_USER+20
    MessageValues ={
    'id': 'int',
    'active' : 'bool'
    }

class ScoreboardRequest(legume.messages.BaseMessage):
    MessageTypeID = legume.messages.BASE_MESSAGETYPEID_USER+4
    MessageValues ={
    'placeholder': 'string 5'
    }

class Scoreboard(legume.messages.BaseMessage):
    MessageTypeID = legume.messages.BASE_MESSAGETYPEID_USER+15
    MessageValues ={
    'scores': 'string 1200'
    }

class PlayerInfo(legume.messages.BaseMessage):
    MessageTypeID = legume.messages.BASE_MESSAGETYPEID_USER+5
    MessageValues ={
    'name': 'string 20',
    'colour': 'int',
    'armor': 'int',
    'speed': 'int',
    'energy': 'int',
    'damage': 'int',
    'speedbullet': 'int',
    'reload': 'int',
    'ability': 'string 15'
    }

class PlayerInfoServer(legume.messages.BaseMessage):
    MessageTypeID = legume.messages.BASE_MESSAGETYPEID_USER+12
    MessageValues ={
    'id': 'int',
    'name': 'string 20',
    'colour': 'int',
    'armor': 'int',
    'speed': 'int',
    'energy': 'int',
    'damage': 'int',
    'speedbullet': 'int',
    'reload': 'int',
    'ability': 'string 15'
    }

class DisconnectNotice(legume.messages.BaseMessage):
    MessageTypeID = legume.messages.BASE_MESSAGETYPEID_USER+6
    MessageValues ={
    'id': 'int'
    }

class ChatMsg(legume.messages.BaseMessage):
    MessageTypeID = legume.messages.BASE_MESSAGETYPEID_USER+7
    MessageValues ={
    'id': 'int',
    'msg': 'string 200',
    'placeholder': 'int'
    }

#Server-side messages
class PlayerPositions(legume.messages.BaseMessage):
    MessageTypeID = legume.messages.BASE_MESSAGETYPEID_USER+8
    MessageValues ={
    'serializedplayerpositions': 'string 1200'
    }

class MapInfo(legume.messages.BaseMessage):
    MessageTypeID = legume.messages.BASE_MESSAGETYPEID_USER+11
    MessageValues ={
    'name': 'string 30',
    'map': 'string 1300',
    'chunks': 'int',
    'chunk': 'int'
    }

class ID(legume.messages.BaseMessage):
    MessageTypeID = legume.messages.BASE_MESSAGETYPEID_USER+13
    MessageValues ={
    'id': 'int'
    }

class Kills(legume.messages.BaseMessage):
    MessageTypeID = legume.messages.BASE_MESSAGETYPEID_USER+17
    MessageValues ={
    'kill': 'string 50'
    }

expletiveslist = ['eviscerated', 'pwned', 'dominated', 'splattered', 'blew up', 'exploded', 'BOOM!', 'POW!', 'slaughtered']
killfeed = []

import re
f = urllib2.urlopen("http://www.canyouseeme.org/")
html_doc = f.read()
f.close()
m = re.search('(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)',html_doc)
pub_ip = repr(m.group(0)).replace("'", "")
print 'Public IP: ' + pub_ip

#print ("Asset: %s " % fqn, "Checking in from IP#: %s " % ext_ip)
int_ip = socket.gethostbyname(socket.getfqdn())
print 'Internal IP: ' + int_ip
server = legume.Server()
try:
    server.listen((str(config['Connection']['bind_IP']), 6385))
    print 'Connected to: ' + str(config['Connection']['bind_IP']) + '    Port: 6385'
except:
    server.listen((int_ip, 6385))
    print 'Connected to: ' + str(int_ip) + '    Port: 6385'

t1 = FetchUrls(server)
t1.start()

server.setTimeout(5)
IPRegistry = {}
PlayerList = []
SenderList = []
playernamelist = []
playerposlist = []
idref = 1

ServerRotation = []
for (dirpath, dirnames, filenames) in walk(os.path.join(mypath, 'Server rotation')):
    ServerRotation.extend(filenames)
    break
MapInfos = MapInfo()
mapstring = base64.b64encode(zlib.compress(json.dumps(pickle.loads(open(os.path.join(mypath, 'Server rotation', ServerRotation[posix]), 'r').read())),9))
my_map = Map(str(ServerRotation[posix][0:-4]), open(os.path.join(mypath, 'Server rotation', ServerRotation[posix]), 'r').read())
numberchunks = len(mapstring)/((len(mapstring)/1200) + 1)
chunk = 0
chunkedmapstring = [''.join(x) for x in zip(*[list(mapstring[z::numberchunks]) for z in range(numberchunks)])]

def custom_msghandler(sender, message):
        global IPRegistry
        global PlayerList
        global chunk
        global chunkedmapstring
        global mapstring
        global numberchunks
        global RocketList
        global idref
        global space
        global masterserver
        if message.MessageTypeID == ArrowStatusMsg.MessageTypeID:
            received_message = str(message.arrows.value)
            #print sender.last_packet_sent_at
            #print str(message.arrows.value)
            IPRegistry[sender.address].a = message.gunorientation.value
            IPRegistry[sender.address].mx = message.mx.value
            if received_message[1] == '1':
                IPRegistry[sender.address].right = True
                #IPRegistry[sender.address].body.velocity += (IPRegistry[sender.address].cachedspeed*30,0)
            else:
                IPRegistry[sender.address].right = False
            if received_message[0] == '1':
                IPRegistry[sender.address].left = True
                #IPRegistry[sender.address].body.velocity -= (IPRegistry[sender.address].cachedspeed*30,0)
            else:
                IPRegistry[sender.address].left = False
            if received_message[2] == '1' and 0 <= IPRegistry[sender.address].body.velocity.y <= 0.01:
                IPRegistry[sender.address].body.velocity += (0,600)
            if received_message[3] == '1' and IPRegistry[sender.address].timer == IPRegistry[sender.address].cachedreloadspeed:
                rocket = Rocket(IPRegistry[sender.address], IPRegistry[sender.address].a, message.mx.value, IPRegistry[sender.address].body.position)
                IPRegistry[sender.address].lastshotid += 1
                IPRegistry[sender.address].lastshot = rocket
                #print len(RocketList)
                #print 'lol'
        if message.MessageTypeID == PlayerInfo.MessageTypeID:
            data = {'cmd': '+p'}
            if ms_public == True:
                r = requests.post(config['Masterserver']['ms_ip'], data)
            spawnpoint = my_map.spawns[random.randint(0, len(my_map.spawns)-1)]
            clientplayer = Playerz(from_pygame((spawnpoint.position_x+65, spawnpoint.position_y+65)), message.colour.value, message.name.value, 100, euclid.Vector2(0, 0))

            clientplayer.reloadspeed = message.reload.value
            clientplayer.weaponvelocity = message.speedbullet.value
            clientplayer.damage = message.damage.value
            clientplayer.armor = message.armor.value
            clientplayer.speed = message.speed.value
            clientplayer.energy = message.energy.value

            clientplayer.checkIfValid()

            clientplayer.cacheddamage = 700 + clientplayer.damage * 25
            clientplayer.cachedvelocity = 15 + clientplayer.weaponvelocity
            clientplayer.cachedreloadspeed = 1500 - clientplayer.reloadspeed * 50
            clientplayer.cachedarmor = clientplayer.armor * 0.03
            clientplayer.cachedspeed = 1 + clientplayer.speed * 0.1
            clientplayer.cachedenergy = 0.1 + clientplayer.energy * 0.1

            clientplayer.ability = message.ability.value

            clientplayer.id = idref
            idref += 1
            IDmsg.id.value = clientplayer.id
            sender.send_reliable_message(IDmsg)

            PlayerInfosx.id.value = clientplayer.id
            PlayerInfosx.name.value = str(clientplayer.name)
            PlayerInfosx.colour.value = clientplayer.colour
            PlayerInfosx.armor.value = clientplayer.armor
            PlayerInfosx.speed.value = clientplayer.speed
            PlayerInfosx.energy.value = clientplayer.energy
            PlayerInfosx.damage.value = clientplayer.damage
            PlayerInfosx.speedbullet.value = clientplayer.weaponvelocity
            PlayerInfosx.reload.value = clientplayer.reloadspeed
            PlayerInfosx.ability.value = str(clientplayer.ability)

            IPRegistry[sender.address] = clientplayer
            print 'New player connected: ' + message.name.value
            PlayerList.append(clientplayer)
            #masterserver.sendall('a')
            playernamelist.append(clientplayer.name)

            while chunk + 1 <= (len(mapstring)/1200) + 1:
                MapInfos.chunks.value = (len(mapstring)/1200) + 1
                MapInfos.chunk.value = chunk
                MapInfos.map.value = chunkedmapstring[chunk]
                MapInfos.name.value = str(ServerRotation[posix])
                sender.send_reliable_message(MapInfos)
                chunk += 1
            chunk = 0

            for platform in my_map.activepowerups:
                PwupMsg.id.value = my_map.powerups.index(platform)
                PwupMsg.active.value = True
                sender.send_reliable_message(PwupMsg)

            for x in SenderList:
                x.send_reliable_message(PlayerInfosx)
                IPRegistry
                PlayerInfoso.id.value = IPRegistry[x.address].id
                PlayerInfoso.name.value = str(IPRegistry[x.address].name)
                PlayerInfoso.colour.value = IPRegistry[x.address].colour
                PlayerInfoso.armor.value = IPRegistry[x.address].armor
                PlayerInfoso.speed.value = IPRegistry[x.address].speed
                PlayerInfoso.energy.value = IPRegistry[x.address].energy
                PlayerInfoso.damage.value = IPRegistry[x.address].damage
                PlayerInfoso.speedbullet.value = IPRegistry[x.address].weaponvelocity
                PlayerInfoso.reload.value = IPRegistry[x.address].reloadspeed
                PlayerInfoso.ability.value = str(IPRegistry[x.address].ability)
                sender.send_reliable_message(PlayerInfoso)

            SenderList.append(sender)
            sender.OnDisconnect += disco_msghandler
            sender.OnError += disco_msghandler
        if message.MessageTypeID == DisconnectNotice.MessageTypeID:
            try:
                if IPRegistry[sender.address] in PlayerList:
                    Disco.id.value = IPRegistry[sender.address].id
                    IPRegistry[sender.address].disconnecting = True
                    print 'Disconnected player: ' + IPRegistry[sender.address].name
                    playernamelist.remove(IPRegistry[sender.address].name)
                    PlayerList.remove(IPRegistry[sender.address])
                    SenderList.remove(sender)
                    space.remove(IPRegistry[sender.address].body, IPRegistry[sender.address].shape)
                    
                    for x in SenderList:
                        x.send_reliable_message(Disco)
                    del IPRegistry[sender.address]
                    sender.disconnect()
                    data = {'cmd': '-p'}
                    if ms_public == True:
                        r = requests.post(config['Masterserver']['ms_ip'], data)
            except:
                pass
        if message.MessageTypeID == ScoreboardRequest.MessageTypeID:
            y = []
            for player in PlayerList:
                x = (player.id, player.score, player.kills, player.deaths)
                y.append(x)
            Scores.scores.value = json.dumps(y)
            sender.send_reliable_message(Scores)
        if message.MessageTypeID == ChatMsg.MessageTypeID:
            if len(''.join(message.msg.value.split())) > 2:
                Chatmessage.id.value = message.id.value
                Chatmessage.msg.value = str(message.msg.value)
                Chatmessage.placeholder.value = message.placeholder.value
                server.send_reliable_message_to_all(Chatmessage)

#def custom_delhandler(sender, args):
#    running = False
#    server.disconnect_all()
#    t1._Thread__stop()
#    server_cmd._Thread__stop()
#    data = {'cmd': '-'}
#    r = requests.post('http://localhost:11080/server', data)

legume.messages.message_factory.add(ArrowStatusMsg)
legume.messages.message_factory.add(PwupStatus)
legume.messages.message_factory.add(ScoreboardRequest)
legume.messages.message_factory.add(Scoreboard)
legume.messages.message_factory.add(PlayerInfo)
legume.messages.message_factory.add(PlayerInfoServer)
legume.messages.message_factory.add(DisconnectNotice)
legume.messages.message_factory.add(ChatMsg)
legume.messages.message_factory.add(PlayerPositions)
legume.messages.message_factory.add(MapInfo)
legume.messages.message_factory.add(ID)
legume.messages.message_factory.add(Kills)

PlayerPositionss = PlayerPositions()
PlayerInfosx = PlayerInfoServer()
PlayerInfoso = PlayerInfoServer()
IDmsg = ID()
Disco = DisconnectNotice()
Scores = Scoreboard()
Killfeedmessage = Kills()
Chatmessage = ChatMsg()
PwupMsg = PwupStatus()

prompt_msg = ''
playernumb = 0
allmsg = ''
oldallmsg = ''
clientplayers = {}
#servertext = open(os.path.join(mypath, 'TXT files', 'ServerSettings.txt'), 'r')
#ServerLines = servertext.readlines()
ServerName = config['Game']['name']
print 'Server name: ' + ServerName

MapName = str(ServerRotation[posix][0:-4])

GameMode = 'DM'

MaxPlayers = int(config['Game']['max_players'])
print 'Max players: ' + str(MaxPlayers) + '\n'

CurrentPlayers = 0

Passworded = False

masterserver_ip = config['Masterserver']['ms_ip']
#masterserver = socket.socket()
#masterserver = SSL.Connection(SSL.Context(SSL.SSLv3_METHOD), socket.socket())
#masterserver.do_handshake_on_connect = True
ms_public = True
if config['Masterserver']['ms_visible'] == 'False':
    #config['Masterserver']['ms_ip'] = ''
    ms_public = False
#try:
#    masterserver.connect((masterserver_ip, 2000))
#    #masterserver.do_handshake()
#    print 'Connected to master server through Internet'
#    print 'Master server IP: ' + str(masterserver_ip)  + '    Port: 2000'
#    ms_connected = True
#except:
#    try:
#        masterserver.connect((int_ip, 2000))
#        print 'Connected to master server through LAN'  + '    Port: 2000'
#        ms_connected = True
#    except:
#        print 'Could not connect to master server. Your game will not be visible on the server list.'
#        print 'Either the master server is down, or your network is not properly configured. Check your firewall and port 2000. Might be a NAT or a LAN problem as well. Cheers.'

#if ms_connected == True:
#    #masterserver.setblocking(1)
#    #masterserver.do_handshake()
#    #masterserver.sendall('r')
#    masterserver.sendall('+' + json.dumps([ServerName, MapName, GameMode, CurrentPlayers, MaxPlayers, Passworded, 'lol'], -1))
data = {'cmd': '+', 'info': json.dumps([ServerName, MapName, GameMode, CurrentPlayers, MaxPlayers, Passworded], -1)}
#createdata = urllib.urlencode(data)
#create = urllib2.Request('http://localhost:11080/server', createdata)
if ms_public == True:
    r = requests.post(config['Masterserver']['ms_ip'], data)
    #masterserver.sendall('a')

server.OnMessage += custom_msghandler
#server.OnDisconnect += custom_delhandler

def disco_msghandler(sender, args):
    global space
    try:
        if IPRegistry[sender.address] in PlayerList:
            Disco.id.value = IPRegistry[sender.address].id
            IPRegistry[sender.address].disconnecting = True
            print 'Disconnected player: ' + IPRegistry[sender.address].name
            playernamelist.remove(IPRegistry[sender.address].name)
            PlayerList.remove(IPRegistry[sender.address])
            SenderList.remove(sender)
            space.remove(IPRegistry[sender.address].body, IPRegistry[sender.address].shape)
            
            for x in SenderList:
                x.send_reliable_message(Disco)
            del IPRegistry[sender.address]
            sender.disconnect()
            data = {'cmd': '-p'}
            if ms_public == True:
                r = requests.post(config['Masterserver']['ms_ip'], data)
    except:
        pass
        #masterserver.sendall('d')

def on_connectcheck(sender, args):
    for x in SenderList:
        if x.address == sender.address:
            sender.disconnect()
while running:  # main game loop
    #server.update()
    #with lock:
    try:
        playerposlist = []
    
        for x in killfeed:
            Killfeedmessage.kill.value = json.dumps(x)
            server.send_reliable_message_to_all(Killfeedmessage)
            killfeed.remove(x)
    
        for player in PlayerList:
            player.move()
            #playerposlist.append((int(player.body.position.x), int(player.body.position.y)))
            if player.lastshotid != 0:
                playerposlist.append((player.id, int(player.body.position.x), int(player.body.position.y), player.health, player.timer, player.a, player.mx, (player.lastshotid,player.lastshot.body.position.int_tuple,(player.lastshot.impulse.x,player.lastshot.impulse.y))))
            else:
                playerposlist.append((player.id, int(player.body.position.x), int(player.body.position.y), player.health, player.timer, player.a, player.mx, (player.lastshotid,0,0)))
    
        PlayerPositionss.serializedplayerpositions.value = json.dumps(playerposlist)
    
        #for peer in server.peers:
            #print peer.last_packet_sent_at
    
        for sender in SenderList:
            if IPRegistry[sender.address].disconnecting == False:
                sender.send_message(PlayerPositionss)
    
        dtime_ms = FPSCLOCK.tick(50)
        dtime = dtime_ms/1000.0
        dfps = 50/(FPSCLOCK.get_fps() + 0.001)
        if dfps > 2:
            dfps = 2
    
        #for s in my_map.powerups:
        #    if s.mode == 2:
        #        sx, sy = s.position_x + 51, s.position_y + 51
        #        if -300 < sx - my_player.body.position.x < 900 and -100 < sy - my_player.body.position.y < 700:
        #            Shield.blit(DISPLAYSURF, (sx - my_player.body.position.x, sy - my_player.body.position.y))
        #        shieldcoll = pygame.Rect(sx - my_player.body.position.x - 16, sy - my_player.body.position.y - 16, 32, 32)
        #        if shieldcoll.colliderect(my_player.rect) and my_player.shielded == False:
        #            SOUNDSDICT['Powa'].play()
        #            my_map.Shields.remove(s)
        #            pygame.time.set_timer(USEREVENT+6, 60000)
        #            my_map.PowerTimes.append((int(pygame.time.get_ticks()) + 60000, 'D'))
        #            my_player.cachedarmor += 0.4
        #            my_player.shielded = True
        #    elif s.mode == 1:
        #        sx, sy = s.position_x + 51, s.position_y + 51
        #        if -300 < sx - my_player.body.position.x < 900 and -100 < sy - my_player.body.position.y < 700:
        #            Speed.blit(DISPLAYSURF, (sx - my_player.body.position.x, sy - my_player.body.position.y))
        #        #DISPLAYSURF.blit(IMAGESDICT['Speed'], (sx - my_player.position.x, sy - my_player.position.y))
        #        speedcoll = pygame.Rect(sx - my_player.body.position.x - 16, sy - my_player.body.position.y - 16, 32, 32)
        #        if speedcoll.colliderect(my_player.rect) and my_player.speeded == False:
        #            SOUNDSDICT['Powa'].play()
        #            my_map.Speeds.remove(s)
        #            pygame.time.set_timer(USEREVENT+7, 60000)
        #            my_map.PowerTimes.append((int(pygame.time.get_ticks()) + 60000, 'S'))
        #            my_player.speedup = 2
        #            my_player.speeded = True
        #
        #    elif s.mode == 0:
        #        sx, sy = s.position_x + 51, s.position_y + 51
        #        px, py = to_pygame(my_player.body.position, DISPLAYSURF)
        #        #DISPLAYSURF.blit(IMAGESDICT['Health'], (sx - my_player.position.x, sy - my_player.position.y))
        #        #if -300 < sx - my_player.body.position.x < 900 and -100 < sy - my_player.body.position.y < 700:
        #        Health.blit(DISPLAYSURF, (sx - px + 400, sy - py + 351))
        #        #s.image.blit(DISPLAYSURF, (sx - px + 400, sy - py + 351))
        #        #healthcoll = pygame.Rect(sx - my_player.body.position.x - 16, sy - my_player.body.position.y - 16, 32, 32)
        #        #if healthcoll.colliderect(my_player.rect) and my_player.health != 100:
        #        #    SOUNDSDICT['Powa'].play()
        #        #    my_map.Healths.remove(s)
        #        #    my_map.PowerTimes.append((int(pygame.time.get_ticks()) + 60000, 'H'))
        #        #    pygame.time.set_timer(21, 60000)
        #        #    if my_player.health <= 75:
        #        #        my_player.health += 25
        #        #    else:
        #        #        my_player.health = 100
        #
        #for x in my_map.PowerTimes:
        #    time, power = x
        #    if time < int(pygame.time.get_ticks()):
        #        if power == 'D':
        #            my_map.Shields.append(my_map.DeletedPowerD[0])
        #            my_player.cachedarmor -= 0.4
        #            my_player.shielded = False
        #            my_map.PowerTimes.remove(x)
        #        if power == 'S':
        #            my_map.Speeds.append(my_map.DeletedPowerS[0])
        #            my_player.speedup = 1
        #            my_player.speeded = False
        #            my_map.PowerTimes.remove(x)
        #        if power == 'H':
        #            my_map.Healths.append(my_map.DeletedPowerH[0])
        #            my_map.PowerTimes.remove(x)
    
        #for platform in my_map.movingplatforms:
        #    platform.body.velocity = Vec2d(platform.lx * math.sin(platform.sx * platform.xxx + platform.ox), platform.ly * math.sin(platform.sy * platform.yyy + platform.oy))
        #    platform.body.position.x += platform.lx * math.sin(platform.sx * platform.xxx + platform.ox) #* dfps
        #    platform.body.position.y -= platform.ly * math.sin(platform.sy * platform.yyy + platform.oy)
        #    platform.yyy += 1
        #    platform.xxx += 1
        #    platform.body.update_position(platform.body, 1/50)
    
        for platform in my_map.deletedpowerups:
            platform.timer += dtime
            #print platform.timer
            if platform.timer > 30:
                platform.timer = 0
                if platform.pwup == 1:
                    platform.parent.cachedspeed -= 1
                if platform.pwup == 2:
                    platform.parent.cachedarmor -= 0.25
                my_map.activepowerups.append(platform)
                my_map.deletedpowerups.remove(platform)
                PwupMsg.id.value = my_map.powerups.index(platform)
                PwupMsg.active.value = True
                server.send_reliable_message_to_all(PwupMsg)
    
        for rocket in RocketList:
            rocket.DisplayRocket()
    
        rocket = 0
        ghostinit = 1
    
        space.step(1.0/50.0)
        for rocket in RocketList:
            rocket.body.reset_forces()

    except KeyboardInterrupt:
        # do nothing here
        running = False
        server.disconnect_all()
        t1._Thread__stop()
        server_cmd._Thread__stop()
        data = {'cmd': '-'}
        if ms_public == True:
            r = requests.post(config['Masterserver']['ms_ip'], data)




