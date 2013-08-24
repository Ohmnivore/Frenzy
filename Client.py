#!/usr/bin/env python2.7
# Frenzy (A 2D Online Myltiplayer Platformer Shooter for Android --- yeah, it's that cool)
# By Mark Beiline ohmnivore.elementfx.com
# Created with PyGame

from pygame.locals import *
import pygame._view
import pygame
import legume
import os
import sys
import random
import math
import cPickle as pickle
import euclid #from https://code.google.com/p/pyeuclid/
import traceback
import threading
import pyganim
import spritesheet
import pygsheet
import pymunk
from pymunk.vec2d import Vec2d
from pymunk.pygame_util import draw_space, from_pygame, to_pygame
from pymunk import Vec2d
import zlib
import base64
import socket
import json
import string
from configobj import ConfigObj
import time

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

#if hasattr(sys,"frozen") and sys.frozen in ("windows_exe", "console_exe"):
#    mypath=jpath.path(os.path.abspath(sys.executable)).dirname()

mypath = module_path()
config = ConfigObj(os.path.join(mypath,'ClientSettings.cfg'))

global FPSCLOCK, DISPLAYSURF, IMAGESDICT, BRUSH, PLAYERIMAGES, running, mx, my, dtime, dtime_ms, drag, n
global moving, n2, colour, rotationCounter, scalingCounter, nameSize, ghostinit, leftReleased, rightReleased
global moving2, aReleased, dReleased, ghostinit2, isOn2, impo1, impo2, n10, lololol, n5, n6, n8, m
global tempx, tempy, tempx2, tempy2, xrect, yrect, xrect2, yrect2, RocketList, rocketdist, sx, sy, reloaded, CloudList
global mapx, mapy, lolx, loly, n
global reloadclock, wind, dfps, noLeft, noRight, lol
global running, mesg, oldmesg, otherplayers, BotsList, otherbot, xdistance, playerbuffer, ArrowStatus, oldmesgpos, sendtimer, sentmsg
mapstring = ''
my_map = None
sentmsg = False
dtime_ms = 0
sendtimer = 0
oldmesgpos = 0
ArrowStatus = ['0', '0', '0', '0']
xdistance = 1000
playerbuffer = 'lol'
BotsList = []
lol = 20
noLeft = False
noRight = False
reloadclock = 0
#gravity = 0.04
lololol = 0
#inAir = False
RocketList = []
reloaded = True
#mypath = os.path.normpath(os.path.dirname(os.path.abspath(sys.argv[0])))
CloudList = []
wind = 2
running = True
mesg = ''
otherplayers = {}
ExploAnimList = []
PowaList = []
groups = 1

displayscores = False
allscores = []
killfeed = []
displaychat = False
chat = '->'
chathistory = []
shifttoggle = False


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
leftReleased = True
rightReleased = True
aReleased = True
dReleased = True
RocketList = []

# Setting of the system icon
icon=pygame.image.load(os.path.join(mypath, 'Images', 'ICO.ico'))
#icon=pygame.image.load('ICO.ico')
pygame.display.set_icon(icon)

# Setting of the caption and global font
pygame.display.set_caption('Frenzy')
BRUSH = pygame.font.Font(os.path.join(mypath, 'Fonts', 'ElectricCity.TTF'), 18)

# Surface object that is drawn to the actual computer screen
DISPLAYSURF = pygame.display.set_mode((WINWIDTH, WINHEIGHT))

#VideoOptions = pickle.load(open(os.path.join(mypath, 'TXT Files', 'VideoOptions.txt'), 'r'))

Crosshairs = pyganim.PygAnimation(pygsheet.spritesheet(os.path.join(mypath, 'Images', 'Crosshairs3.png')).load_strip((0,0,100,100), 8, colorkey = (204, 204, 204), time = 0.05))
Crosshairs.play()

Health = pyganim.PygAnimation(pygsheet.spritesheet(os.path.join(mypath, 'Images', 'HoloHealthSprite2.png')).load_strip((0,0,32,32), 7, colorkey = (0, 0, 0), time = 0.07))
Health.play()

Shield = pyganim.PygAnimation(pygsheet.spritesheet(os.path.join(mypath, 'Images', 'HoloBatterySprite.png')).load_strip((0,0,32,32), 7, colorkey = (0, 0, 0), time = 0.07))
Shield.play()

Speed = pyganim.PygAnimation(pygsheet.spritesheet(os.path.join(mypath, 'Images', 'HoloSpeedSprite.png')).load_strip((0,0,32,32), 7, colorkey = (0, 0, 0), time = 0.07))
Speed.play()

ScientistRight = pyganim.PygAnimation(pygsheet.spritesheetalpha(os.path.join(mypath, 'Images', 'PlayerGreen.png')).load_strip((0,0,37,45), 11, colorkey = (14, 24, 45), time = 0.05))
ScientistRight.play()
ScientistRight.reverse()
ScientistRight.flip(True, False)
ScientistRightRev = ScientistRight.getCopy()
ScientistRightRev.reverse()
ScientistRightRev.play()
ScientistRightImmo = pygame.image.load(os.path.join(mypath, 'Images', 'scientistrightimmo.png')).convert_alpha()

ScientistLeft = pyganim.PygAnimation(pygsheet.spritesheetalpha(os.path.join(mypath, 'Images', 'PlayerGreen.png')).load_strip((0,0,37,45), 11, colorkey = (14, 24, 45), time = 0.05))
ScientistLeft.reverse()
ScientistLeft.play()
ScientistLeftRev = ScientistLeft.getCopy()
ScientistLeftRev.reverse()
ScientistLeftRev.play()
ScientistLeftImmo = pygame.image.load(os.path.join(mypath, 'Images', 'scientistleftimmo.png')).convert_alpha()

ScientistGreen = {
              'Right' : ScientistRight,
              'RightRev' : ScientistRightRev,
              'RightImmo' : ScientistRightImmo,
              'Left' : ScientistLeft,
              'LeftRev' : ScientistLeftRev,
              'LeftImmo' : ScientistLeftImmo,
}

ScientistRightBlue = pyganim.PygAnimation(pygsheet.spritesheetalpha(os.path.join(mypath, 'Images', 'PlayerBlue.png')).load_strip((0,0,37,45), 11, colorkey = (14, 24, 45), time = 0.05))
ScientistRightBlue.play()
ScientistRightBlue.flip(True, False)
ScientistRightBlue.reverse()
ScientistRightRevBlue = ScientistRightBlue.getCopy()
ScientistRightRevBlue.reverse()
ScientistRightRevBlue.play()
ScientistRightImmoBlue = pygame.image.load(os.path.join(mypath, 'Images', 'scientistrightimmoblue.png')).convert_alpha()

ScientistLeftBlue = pyganim.PygAnimation(pygsheet.spritesheetalpha(os.path.join(mypath, 'Images', 'PlayerBlue.png')).load_strip((0,0,37,45), 11, colorkey = (14, 24, 45), time = 0.05))
ScientistLeftBlue.reverse()
ScientistLeftBlue.play()
ScientistLeftRevBlue = ScientistLeftBlue.getCopy()
ScientistLeftRevBlue.reverse()
ScientistLeftRevBlue.play()
ScientistLeftImmoBlue = pygame.image.load(os.path.join(mypath, 'Images', 'scientistleftimmoblue.png')).convert_alpha()

ScientistBlue = {
              'Right' : ScientistRightBlue,
              'RightRev' : ScientistRightRevBlue,
              'RightImmo' : ScientistRightImmoBlue,
              'Left' : ScientistLeftBlue,
              'LeftRev' : ScientistLeftRevBlue,
              'LeftImmo' : ScientistLeftImmoBlue,
}

ScientistRightRed = pyganim.PygAnimation(pygsheet.spritesheetalpha(os.path.join(mypath, 'Images', 'PlayerRed.png')).load_strip((0,0,37,45), 11, colorkey = (14, 24, 45), time = 0.05))
ScientistRightRed.play()
ScientistRightRed.flip(True, False)
ScientistRightRed.reverse()
ScientistRightRevRed = ScientistRightRed.getCopy()
ScientistRightRevRed.reverse()
ScientistRightRevRed.play()
ScientistRightImmoRed = pygame.image.load(os.path.join(mypath, 'Images', 'scientistrightimmored.png')).convert_alpha()

ScientistLeftRed = pyganim.PygAnimation(pygsheet.spritesheetalpha(os.path.join(mypath, 'Images', 'PlayerRed.png')).load_strip((0,0,37,45), 11, colorkey = (14, 24, 45), time = 0.05))
ScientistLeftRed.reverse()
ScientistLeftRed.play()
ScientistLeftRevRed = ScientistLeftRed.getCopy()
ScientistLeftRevRed.reverse()
ScientistLeftRevRed.play()
ScientistLeftImmoRed = pygame.image.load(os.path.join(mypath, 'Images', 'scientistleftimmored.png')).convert_alpha()

ScientistRed = {
              'Right' : ScientistRightRed,
              'RightRev' : ScientistRightRevRed,
              'RightImmo' : ScientistRightImmoRed,
              'Left' : ScientistLeftRed,
              'LeftRev' : ScientistLeftRevRed,
              'LeftImmo' : ScientistLeftImmoRed,
}

ScientistRightYellow = pyganim.PygAnimation(pygsheet.spritesheetalpha(os.path.join(mypath, 'Images', 'PlayerYellow.png')).load_strip((0,0,37,45), 11, colorkey = (14, 24, 45), time = 0.05))
ScientistRightYellow.play()
ScientistRightYellow.flip(True, False)
ScientistRightYellow.reverse()
ScientistRightRevYellow = ScientistRightYellow.getCopy()
ScientistRightRevYellow.reverse()
ScientistRightRevYellow.play()
ScientistRightImmoYellow = pygame.image.load(os.path.join(mypath, 'Images', 'scientistrightimmoyellow.png')).convert_alpha()

ScientistLeftYellow = pyganim.PygAnimation(pygsheet.spritesheetalpha(os.path.join(mypath, 'Images', 'PlayerYellow.png')).load_strip((0,0,37,45), 11, colorkey = (14, 24, 45), time = 0.05))
ScientistLeftYellow.reverse()
ScientistLeftBlue.play()
ScientistLeftRevYellow = ScientistLeftYellow.getCopy()
ScientistLeftRevYellow.reverse()
ScientistLeftRevYellow.play()
ScientistLeftImmoYellow = pygame.image.load(os.path.join(mypath, 'Images', 'scientistleftimmoyellow.png')).convert_alpha()

ScientistYellow = {
              'Right' : ScientistRightYellow,
              'RightRev' : ScientistRightRevYellow,
              'RightImmo' : ScientistRightImmoYellow,
              'Left' : ScientistLeftYellow,
              'LeftRev' : ScientistLeftRevYellow,
              'LeftImmo' : ScientistLeftImmoYellow,
}

PLAYERANIMS = [ScientistGreen, ScientistBlue, ScientistRed, ScientistYellow]

Gun = pygame.image.load(os.path.join(mypath, 'Images', 'gunsquare.png')).convert_alpha()
GunReverse = pygame.transform.flip(Gun, True, False)

BlueBullet = pyganim.PygAnimation(pygsheet.spritesheetalpha(os.path.join(mypath, 'Effects', 'Bullet', 'BlueBulletTransparent5.png')).load_strip((0,0,37,37), 8, colorkey = (255,255,255), time = 0.04))
BlueBullet.set_colorkey(black)
BlueBullet.play()

GreenBullet = pyganim.PygAnimation(pygsheet.spritesheetalpha(os.path.join(mypath, 'Effects', 'Bullet', 'GreenBulletTransparent5.png')).load_strip((0,0,37,37), 8, colorkey = (255,255,255), time = 0.04))
GreenBullet.set_colorkey(black)
GreenBullet.play()

RedBullet = pyganim.PygAnimation(pygsheet.spritesheetalpha(os.path.join(mypath, 'Effects', 'Bullet', 'RedBulletTransparent5.png')).load_strip((0,0,37,37), 8, colorkey = (255,255,255), time = 0.04))
RedBullet.set_colorkey(black)
RedBullet.play()

YellowBullet = pyganim.PygAnimation(pygsheet.spritesheetalpha(os.path.join(mypath, 'Effects', 'Bullet', 'YellowBulletTransparent5.png')).load_strip((0,0,37,37), 8, colorkey = (255,255,255), time = 0.04))
YellowBullet.set_colorkey(black)
YellowBullet.play()

GreenExplo = pyganim.PygAnimation(pygsheet.spritesheetalpha(os.path.join(mypath, 'Images', 'ExploGreen.png')).load_strip((0,0,256,256), 20, colorkey = (0,0,0), time = 0.03))
#GreenExplo.set_colorkey(black)

BlueExplo = pyganim.PygAnimation(pygsheet.spritesheetalpha(os.path.join(mypath, 'Images', 'ExploBlue.png')).load_strip((0,0,256,256), 20, colorkey = (0,0,0), time = 0.03))
#BlueExplo.set_colorkey(black)

RedExplo = pyganim.PygAnimation(pygsheet.spritesheetalpha(os.path.join(mypath, 'Images', 'ExploRed.png')).load_strip((0,0,256,256), 20, colorkey = (0,0,0), time = 0.03))
#RedExplo.set_colorkey(black)

YellowExplo = pyganim.PygAnimation(pygsheet.spritesheetalpha(os.path.join(mypath, 'Images', 'ExploYellow.png')).load_strip((0,0,256,256), 20, colorkey = (0,0,0), time = 0.03))
#YellowExplo.set_colorkey(black)

RectBlocks = spritesheet.spritesheet(os.path.join(mypath, 'Images', 'RectBlocks.png')).load_strip((0,0,171,22), 16, colorkey = (51, 51, 51))
SquareBlocks = spritesheet.spritesheet(os.path.join(mypath, 'Images', 'SquareBlocks.png')).load_strip((0,0,168,171), 16, colorkey = (51, 51, 51))

ArmorAnimRight = pyganim.PygAnimation(pygsheet.spritesheet(os.path.join(mypath, 'Images', 'armoranimright.png')).load_strip((0,0,37,45), 11, colorkey = (14, 24, 45), time = 0.05))
ArmorAnimRight.play()

ArmorAnimLeft = pyganim.PygAnimation(pygsheet.spritesheet(os.path.join(mypath, 'Images', 'armoranimleft.png')).load_strip((0,0,37,45), 11, colorkey = (14, 24, 45), time = 0.05))
ArmorAnimLeft.reverse()
ArmorAnimLeft.play()
ArmorAnimLeft.fastForward(0.15)

SpeedAnimRight = pyganim.PygAnimation(pygsheet.spritesheet(os.path.join(mypath, 'Images', 'speedright.png')).load_strip((0,0,37,45), 11, colorkey = (14, 24, 45), time = 0.05))
SpeedAnimRight.play()
#SpeedAnimRight.nextFrame(jump=6)

SpeedAnimLeft = pyganim.PygAnimation(pygsheet.spritesheet(os.path.join(mypath, 'Images', 'speedleft.png')).load_strip((0,0,37,45), 11, colorkey = (14, 24, 45), time = 0.05))
SpeedAnimLeft.reverse()
SpeedAnimLeft.play()
#SpeedAnimLeft.nextFrame(jump=6)

Heartbeat = pyganim.PygAnimation(pygsheet.spritesheetalpha(os.path.join(mypath, 'Effects', 'Heart-beat', 'HeartBeatLoopTransparent.png')).load_strip((0,0,256,256), 8, colorkey = (14, 24, 45), time = 0.05))
#Heartbeat.convert_alpha()
Heartbeat.play()

Cloak = pyganim.PygAnimation(pygsheet.spritesheetalpha(os.path.join(mypath, 'Effects', 'Cloak', 'CloakTransparent.png')).load_strip((0,0,128,128), 8, colorkey = (14, 24, 45), time = 0.05))
#Heartbeat.convert_alpha()
Cloak.play()
#Cloak.loop = False

Cloak2 = pyganim.PygAnimation(pygsheet.spritesheetalpha(os.path.join(mypath, 'Effects', 'Cloak', 'CloakTransparent.png')).load_strip((0,0,128,128), 8, colorkey = (14, 24, 45), time = 0.05))
#Heartbeat.convert_alpha()
Cloak2.play()
#Heartbeat.convert_alpha()
#Cloak2.play()
Cloak2.loop = False

DeathExplo = pyganim.PygAnimation(pygsheet.spritesheetalpha(os.path.join(mypath, 'Effects', 'Death', 'DeathTransparent.png')).load_strip((0,0,256,256), 8, colorkey = (14, 24, 45), time = 0.05))
#Heartbeat.convert_alpha()
DeathExplo.play()

Heal = pyganim.PygAnimation(pygsheet.spritesheetalpha(os.path.join(mypath, 'Effects', 'Heal', 'HealLoopTransparent.png')).load_strip((0,0,256,256), 8, colorkey = (14, 24, 45), time = 0.05))
#Heartbeat.convert_alpha()
Heal.play()

Circle = pyganim.PygAnimation(pygsheet.spritesheetalpha(os.path.join(mypath, 'Effects', 'Loading', 'CircleTransparent.png')).load_strip((0,0,256,256), 8, colorkey = (14, 24, 45), time = 0.05))
#Heartbeat.convert_alpha()
Circle.play()

Powerup = pyganim.PygAnimation(pygsheet.spritesheetalpha(os.path.join(mypath, 'Effects', 'Powerup', 'PowerupTransparent.png')).load_strip((0,0,126,119), 8, colorkey = (14, 24, 45), time = 0.03))
#Heartbeat.convert_alpha()
Powerup.play()
Powerup.loop = False

#BlueExplo = pyganim.PygAnimation(pygsheet.spritesheet(os.path.join(mypath, 'Images', 'ExploBlueBlack.png')).load_strip((0,0,256,256), 20, colorkey = (0,0,0), time = 0.03))
#BlueExplo.set_colorkey(black)

ShieldAbility = pyganim.PygAnimation(pygsheet.spritesheetalpha(os.path.join(mypath, 'Effects', 'Shield', 'Shield2.png')).load_strip((0,0,80,80), 8, colorkey = (14, 24, 45), time = 0.05))
#Heartbeat.convert_alpha()
ShieldAbility.play()

ShieldStart = pyganim.PygAnimation(pygsheet.spritesheetalpha(os.path.join(mypath, 'Effects', 'Shield', 'ShieldStartTransparent.png')).load_strip((0,0,128,128), 8, colorkey = (14, 24, 45), time = 0.05))
#Heartbeat.convert_alpha()
#ShieldStart.play()

Timezone = pyganim.PygAnimation(pygsheet.spritesheetalpha(os.path.join(mypath, 'Effects', 'Timezone', 'TimezoneLoopTransparent.png')).load_strip((0,0,256,256), 8, colorkey = (14, 24, 45), time = 0.05))
#Heartbeat.convert_alpha()
Timezone.play()

ABILITYDICT = {
                'Heartbeat' : Heartbeat,
                'Cloak' : Cloak2,
                'Heal' : Heal,
                'Shield' : ShieldAbility,
                'Timezone' : Timezone
}

BULLETS = [GreenBullet, BlueBullet, RedBullet, YellowBullet]
EXPLOS = [GreenExplo, BlueExplo, RedExplo, YellowExplo]
#PLAYERANIMS = {
#              'ScientistRight'
#}

# A global dict value that will contain all the Pygame
# Surface objects returned by pygame.image.load().
IMAGESDICT = {#'Player' : pygame.image.load('GreenSquare.png'),
              'ArmorRight' : pygame.image.load(os.path.join(mypath, 'Images', 'armorright.png')).convert(),
              'ArmorLeft' : pygame.image.load(os.path.join(mypath, 'Images', 'armorleft.png')).convert(),
              'SpeedRight' : pygame.image.load(os.path.join(mypath, 'Images', 'speedrightimmo.png')).convert(),
              'SpeedLeft' : pygame.image.load(os.path.join(mypath, 'Images', 'speedleftimmo.png')).convert(),
              'PackRight' : pygame.image.load(os.path.join(mypath, 'Images', 'PackRight.png')).convert_alpha(),
              'PackLeft' : pygame.image.load(os.path.join(mypath, 'Images', 'PackLeft.png')).convert_alpha(),
              'MovingDanger' : pygame.image.load(os.path.join(mypath, 'Images', 'dangermoving.png')).convert(),
              'Background' : pygame.image.load(os.path.join(mypath, 'Backgrounds', config['Video']['background'])).convert()}

animatebck = False

if len(config['Video']['animated_background']) > 0:
    animatebck = True
    widthbcka = int(config['Video']['animated_background_width'])
    bckaframes = int(config['Video']['animated_background_frames'])
    secperframe = float(config['Video']['animated_background_sec/frame'])
    bckgroundwidth = widthbcka
    IMAGESDICT['Background'] = pyganim.PygAnimation(pygsheet.spritesheetalpha(os.path.join(mypath, 'Backgrounds', config['Video']['animated_background'])).load_strip((0,0, widthbcka,600), bckaframes, colorkey = (14, 24, 45), time = secperframe))
    IMAGESDICT['Background'].play()
bckground2 = pygame.image.load(os.path.join(mypath, 'Backgrounds', config['Video']['background'])).convert()
#bckgroundwidth = IMAGESDICT['Background'].get_width()
bckgroundwidth2 = bckground2.get_width()
#pygame.image.save(IMAGESDICT['MovingDanger'], 'movingdanger.png')

IMAGESDICT['MovingDanger'].set_colorkey((51,51,51))
IMAGESDICT['ArmorRight'].set_colorkey((14, 24, 45))
IMAGESDICT['ArmorLeft'].set_colorkey((14, 24, 45))
IMAGESDICT['SpeedRight'].set_colorkey((14, 24, 45))
IMAGESDICT['SpeedLeft'].set_colorkey((14, 24, 45))

#IMAGESDICT['Health'].set_colorkey((255,255,255))
#IMAGESDICT['Health'].set_alpha(160, pygame.RLEACCEL)

#IMAGESDICT['MovingDanger'].set_colorkey((51,51,51))

# COLORS is a list of all possible colors.
COLORS = [green, blue,
                red, yellow]

##Particle effects (PyIgnition)
#fire = PyIgnition.ParticleEffect(DISPLAYSURF, (0, 0), (800, 600))
##gravity = fire.CreateDirectedGravity(strength = 0.07, direction = [0, -1])
##wind = fire.CreateDirectedGravity(strength = 0.05, direction = [1, 0])
#source = fire.CreateSource((300, 500), initspeed = 2.0, initdirection = 0.0, initspeedrandrange = 1.0, initdirectionrandrange = 0.5, particlesperframe = 10, particlelife = 100, drawtype = PyIgnition.DRAWTYPE_CIRCLE, colour = (255, 200, 100), radius = 3.0)
#source.CreateParticleKeyframe(10, colour = (200, 50, 20), radius = 4.0)
#source.CreateParticleKeyframe(30, colour = (150, 0, 0), radius = 6.0)
#source.CreateParticleKeyframe(60, colour = (50, 20, 20), radius = 20.0)
#source.CreateParticleKeyframe(80, colour = (0, 0, 0), radius = 50.0)
#fire.SaveToFile("Fire.ppe")



# Loading the music
pygame.mixer.music.load(os.path.join(mypath, 'Tracks', random.choice(os.listdir(os.path.join(mypath, 'Tracks')))))
pygame.mixer.music.play()

SONGFINISHED = USEREVENT+25
#songfinishedevent = pygame.event.Event(SONGFINISHED)

pygame.mixer.music.set_endevent(SONGFINISHED)

#SoundSettings = pickle.load(open(os.path.join(mypath, 'TXT Files', 'AudioOptions.txt'), 'r'))
MusicVolume = int(config['Audio']['music'])
#if MusicVolume == 0:
#    MusicVolume = 1
EffectsVolume = int(config['Audio']['effects'])
#if EffectsVolume == 0:
#    EffectsVolume = 1

pygame.mixer.music.set_volume(0.7 * MusicVolume/100)

# Loading the sounds
SOUNDSDICT = {'Jump' : pygame.mixer.Sound(os.path.join(mypath, 'Sounds', 'Jump2.ogg')),
              'Dead' : pygame.mixer.Sound(os.path.join(mypath, 'Sounds', 'Dead.ogg')),
              'Boom' : pygame.mixer.Sound(os.path.join(mypath, 'Sounds', 'Boom.ogg')),
              'Hit' : pygame.mixer.Sound(os.path.join(mypath, 'Sounds', 'Hit.ogg')),
              'Kill' : pygame.mixer.Sound(os.path.join(mypath, 'Sounds', 'Kill.ogg')),
              'Explosion' : pygame.mixer.Sound(os.path.join(mypath, 'Sounds', 'Explosion.ogg')),
              'Powa' : pygame.mixer.Sound(os.path.join(mypath, 'Sounds', 'Powa.ogg')),}

# Setting sounds' volumes
SOUNDSDICT['Jump'].set_volume(0.3 * EffectsVolume/100)
SOUNDSDICT['Boom'].set_volume(0.3 * EffectsVolume/100)
SOUNDSDICT['Dead'].set_volume(0.6 * EffectsVolume/100)
SOUNDSDICT['Powa'].set_volume(0.6 * EffectsVolume/100)
SOUNDSDICT['Explosion'].set_volume(1 * EffectsVolume/100)

# The variable that keeps the main loop running
running = True

# A variable to determine if the user is moving the player
moving = False

# Set key repeat to repeatable
pygame.key.set_repeat(1, 8)

# Counters for rotation and scaling
rotationCounter = 0
scalingCounter = 0

# Hide the cursor
pygame.mouse.set_visible(0)

SENDTIMER = USEREVENT + 7
sendtimerevent = pygame.event.Event(SENDTIMER)
pygame.event.post(sendtimerevent)
pygame.time.set_timer(USEREVENT + 7, 100)

RELOADUSER = USEREVENT+3
reloadevent = pygame.event.Event(RELOADUSER)
pygame.event.post(reloadevent)

#CLOUDTIMER = USEREVENT+4
#cloudtimerevent = pygame.event.Event(CLOUDTIMER)
#pygame.event.post(cloudtimerevent)
#pygame.time.set_timer(USEREVENT+4, 5000 * 3/wind)

WINDRESET = USEREVENT+5
windresetevent = pygame.event.Event(WINDRESET)
pygame.event.post(windresetevent)
pygame.time.set_timer(USEREVENT+5, 30000)

SHIELDRESET = USEREVENT+6
shieldresetevent = pygame.event.Event(SHIELDRESET)

# Set events for left and right key presses
LEFTGHOST = USEREVENT+2
ghostleft = pygame.event.Event(LEFTGHOST)
pygame.event.post(ghostleft)

RIGHTGHOST = USEREVENT+1
ghostright = pygame.event.Event(RIGHTGHOST)
pygame.event.post(ghostright)

ghostinit = 0

space = pymunk.Space()
space.gravity = (0.0, -700.0)
space.collision_slop = 0.0001
space.collision_bias = pow(1.0-0.1, 120.0)
#space.add_collision_handler()

def textHollow(font, message, fontcolor):
    notcolor = [c^0xFF for c in fontcolor]
    base = font.render(message, 0, fontcolor, notcolor)
    size = base.get_width() + 2, base.get_height() + 2
    img = pygame.Surface(size, 16)
    img.fill(notcolor)
    base.set_colorkey(0)
    img.blit(base, (0, 0))
    img.blit(base, (2, 0))
    img.blit(base, (0, 2))
    img.blit(base, (2, 2))
    base.set_colorkey(0)
    base.set_palette_at(1, notcolor)
    img.blit(base, (1, 1))
    img.set_colorkey(notcolor)
    return img

def textOutline(font, message, fontcolor, outlinecolor):
    base = font.render(message, 0, fontcolor)
    outline = textHollow(font, message, outlinecolor)
    img = pygame.Surface(outline.get_size(), 16)
    img.blit(base, (1, 1))
    img.blit(outline, (0, 0))
    img.set_colorkey(0)
    return img

# The Platform class represents
#class Platform:
#
#    def __init__(self, position_x, position_y, colour = random.randint(0, 3), char = '#'):
#        self.position_x = position_x
#        self.position_y = position_y
#        self.colour = colour
#        self.char = char
#        self.block = 1
#        #self.block = random.choice(RectBlocks)

class Platform:
    def __init__(self, position_x, position_y, variety, mode):
        self.position_x = position_x
        self.position_y = position_y
        self.type = variety
        self.mode = mode
        self.bound = None
        self.image = None
        self.body = None
        self.shape = None
        self.pwup = 0


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
        self.activepwups = []
        for x in json.loads(maptext):
            if self.lowest_y < x[1]:
                self.lowest_y = x[1] + 300
            platform = Platform(x[0], x[1], x[2], x[3])
            platform.mode = x[3]
            if x[2] == 0:
                platform.image = random.choice(RectBlocks)
                platform.bound = Rect(x[0], x[1], 168, 22)
                platform.body = pymunk.Body()
                platform.body.position = from_pygame(Vec2d(platform.position_x, platform.position_y), DISPLAYSURF)
                xp, yp = platform.bound.topleft
                width = platform.bound.width
                height = platform.bound.height
                platform.shape = pymunk.Poly(space.static_body, [from_pygame(Vec2d(xp,yp), DISPLAYSURF), from_pygame(Vec2d(xp+width,yp), DISPLAYSURF), from_pygame(Vec2d(xp+width,yp+height), DISPLAYSURF), from_pygame(Vec2d(xp,yp+height), DISPLAYSURF)])
                platform.shape.friction = 2.4
                space.add(platform.shape)
                self.platforms.append(platform)

            if x[2] == 1:
                platform.image = random.choice(SquareBlocks)
                platform.bound = Rect(x[0], x[1], 168, 168)
                platform.body = pymunk.Body()
                platform.body.position = from_pygame(Vec2d(platform.position_x, platform.position_y), DISPLAYSURF)
                xp, yp = platform.bound.topleft
                width = platform.bound.width
                height = platform.bound.height
                platform.shape = pymunk.Poly(space.static_body, [from_pygame(Vec2d(xp,yp), DISPLAYSURF), from_pygame(Vec2d(xp+width,yp), DISPLAYSURF), from_pygame(Vec2d(xp+width,yp+height), DISPLAYSURF), from_pygame(Vec2d(xp,yp+height), DISPLAYSURF)])
                platform.shape.friction = 2.4
                space.add(platform.shape)
                self.platforms.append(platform)
            if x[2] == 2:
                platform.image = IMAGESDICT['MovingDanger']
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
                platform.body.position = from_pygame(Vec2d(platform.position_x, platform.position_y), DISPLAYSURF)
                xp, yp = platform.bound.topleft
                width = platform.bound.width
                height = platform.bound.height
                platform.shape = pymunk.Poly(space.static_body, [from_pygame(Vec2d(xp,yp), DISPLAYSURF), from_pygame(Vec2d(xp+width,yp), DISPLAYSURF), from_pygame(Vec2d(xp+width,yp+height), DISPLAYSURF), from_pygame(Vec2d(xp,yp+height), DISPLAYSURF)])
                platform.shape.friction = 2.4
                space.add(platform.shape)
                self.platforms.append(platform)
                self.movingplatforms.append(platform)
                platform.body.apply_force(Vec2d(0.0, 700.0))
            if x[2] == 3:
                platform.bound = Rect(x[0], x[1], 168, 168)
                platform.body = pymunk.Body()
                platform.body.position = from_pygame(Vec2d(platform.position_x, platform.position_y), DISPLAYSURF)
                self.spawns.append(platform)
                self.spawnlist.append(platform.shape)
            if x[2] == 4:
                platform.bound = Rect(x[0], x[1], 168, 168)
                platform.body = pymunk.Body()
                platform.body.position = from_pygame(Vec2d(platform.position_x, platform.position_y), DISPLAYSURF)
                xp, yp = platform.bound.topleft
                width = platform.bound.width
                height = platform.bound.height
                platform.shape = pymunk.Poly(space.static_body, [from_pygame(Vec2d(xp,yp), DISPLAYSURF), from_pygame(Vec2d(xp+width,yp), DISPLAYSURF), from_pygame(Vec2d(xp+width,yp+height), DISPLAYSURF), from_pygame(Vec2d(xp,yp+height), DISPLAYSURF)])
                platform.shape.friction = 0.0
                platform.shape.sensor = True
                space.add(platform.shape)
                if x[3] == 0:
                    #platform.image = IMAGESDICT['Health']
                    platform.pwup = 0
                if x[3] == 1:
                    #platform.image = IMAGESDICT['Speed']
                    platform.pwup = 1
                if x[3] == 2:
                    #print 'Shield'
                    #platform.image = IMAGESDICT['Shield']
                    platform.pwup = 2
                self.powerups.append(platform)
                self.poweruplist.append(platform.shape)



    def DrawFromText(self):
        pass

# The player class: represents the controllable character on screen
class Playerz:

    def __init__(self, position, colour, name , health , velocity): # Constructor
        #self.PlayerInfo = open(os.path.join(mypath, 'TXT Files', 'PlayerInfo.txt'), 'r')
        global space, groups
        #self.PlayerInfo = pickle.load(open(os.path.join(mypath, 'TXT Files', 'PlayerInfo.txt'), 'r'))
        #INFO = self.PlayerInfo.readlines()
        self.AIrect = Rect(0,0,700, 500)
        self.alreadycreated = 0
        #self.newstr = INFO[0].replace("\n", "")
        if name == 'init':
            self.id = 1
            self.name = config['Player']['name']
            self.colour = int(config['Player']['color'])
            self.reloadspeed = int(config['Player']['g_reload'])
            self.weaponvelocity = int(config['Player']['g_speed'])
            self.damage = int(config['Player']['g_dmg'])
            self.cacheddamage = 700 + self.damage * 25
            self.cachedvelocity = 15 + self.weaponvelocity
            self.cachedreloadspeed = 1500 - self.reloadspeed * 50

            self.armor = int(config['Player']['p_armor'])
            self.speed = int(config['Player']['p_speed'])
            self.energy = int(config['Player']['p_energy'])
            self.ability = config['Player']['ability'].capitalize()
            self.cachedarmor = self.armor * 0.03
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
        else:
            self.id = 1
            self.colour = colour
            self.name = name
            self.ability = 'Cloak'
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
        self.mx = False
        self.abilitystatus = False
        self.a = 1
        self.position = position
        #self.colour = int(INFO[1])
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
        self.body.position = from_pygame(self.position, DISPLAYSURF)
        self.shape = pymunk.Poly(self.body, [(0,40), (40,40), (40,0), (0,0)])
        self.shape.friction = 0.1
        self.shape.elasticity = 0.0
        self.shape.group = groups
        groups += 1
        self.oldvelocity = self.body.velocity
        #self.shape.group = 1
        space.add(self.body, self.shape)
        self.timer = 0
        self.cachedname = 0
        if name != 'Bot':
            if int(self.colour) == 0:
                #self.cachedname = BRUSH.render(INFO[0].replace("\n", ""), True, (153,204,0))
                self.cachedname = textOutline(BRUSH, self.name, (153,204,0),(0,0,2))
            if int(self.colour) == 1:
                #self.cachedname = BRUSH.render(INFO[0].replace("\n", ""), True, (94,165,199))
                self.cachedname = textOutline(BRUSH, self.name, (94,165,199),(0,0,2))
            if int(self.colour) == 2:
                #self.cachedname = BRUSH.render(INFO[0].replace("\n", ""), True, (191,59,42))
                self.cachedname = textOutline(BRUSH, self.name, (191,59,42),(0,0,2))
            if int(self.colour) == 3:
                #self.cachedname = BRUSH.render(INFO[0].replace("\n", ""), True, (255,255,0))
                self.cachedname = textOutline(BRUSH, self.name, (255,255,0),(0,0,2))

    def checkIfValid(self):
        if self.reloadspeed + self.weaponvelocity + self.damage > 15:
            self.reloadspeed, self.weaponvelocity, self.damage = 0
        if self.armor + self.speed + self.energy > 15:
            self.armor, self.speed, self.energy = 0

    def display(self):
        global dtime_ms
        rx = int(379)
        ry = int(279)
        #DISPLAYSURF.blit(PLAYERIMAGES[self.colour], (rx,ry))
        pygame.draw.rect(DISPLAYSURF, black, Rect((rx - 21,ry - 12 - 15),(78, 8)))
        pygame.draw.rect(DISPLAYSURF, red, Rect((rx - 18,ry - 9 - 15),(78, 6)))
        if self.health > 100:
            self.health = 100
        pygame.draw.rect(DISPLAYSURF, green, Rect((rx - 18,ry - 9 - 15),(78*(self.health/100), 6)))
        nameSize = BRUSH.size(self.name)
        DISPLAYSURF.blit(self.cachedname, (rx + ((42 - nameSize[0])/2), ry - 33 - 20))
        #DISPLAYSURF.blit(BRUSH.render(str(FPSCLOCK.get_fps()), True, (255,255,255)), (5, 5))
        DISPLAYSURF.blit(textOutline(BRUSH, str(int(FPSCLOCK.get_fps())), (255,255,255),(0,0,2)), (5, 5))
        #nameSize = BRUSH.size(self.name)

        pygame.draw.rect(DISPLAYSURF, black, Rect((rx - 21,ry - 12),(78, 8)))
        global reloadclock
        if self.timer > self.cachedreloadspeed - 1:
            self.timer = self.cachedreloadspeed
        float(self.timer)
        self.timer += dtime_ms
        timerbuffer = self.timer
        if timerbuffer > self.cachedreloadspeed:
            timerbuffer = self.cachedreloadspeed
        pygame.draw.rect(DISPLAYSURF, yellow, Rect((rx - 18,ry - 9),(78*(float(timerbuffer/float(self.cachedreloadspeed))), 6)))

    def displayBot(self):
        self.hitbox.topleft = (self.position.x + 379, self.position.y + 600)
        rx = self.position.x
        ry = self.position.y
        #+ euclid.Vector2(379, 279)
        DISPLAYSURF.blit(PLAYERIMAGES[self.colour], (rx - my_player.position.x + 379,ry - my_player.position.y + 279 + 600))
        pygame.draw.rect(DISPLAYSURF, black, Rect((rx - 21 - my_player.position.x + 379,ry - 12 - 15 - my_player.position.y + 279 + 600),(78, 8)))
        pygame.draw.rect(DISPLAYSURF, red, Rect((rx - 18 - my_player.position.x + 379,ry - 9 - 15 - my_player.position.y + 279 + 600),(78, 6)))
        pygame.draw.rect(DISPLAYSURF, green, Rect((rx - 18 - my_player.position.x + 379,ry - 9 - 15 - my_player.position.y + 279 + 600),(78*(self.health/100), 6)))
        nameSize = BRUSH.size(self.name)
        DISPLAYSURF.blit(self.cachedname, (rx + ((42 - nameSize[0])/2) - my_player.position.x + 379, ry - 33 - 20 - my_player.position.y))
        #DISPLAYSURF.blit(BRUSH.render(str(FPSCLOCK.get_fps()), True, (255,255,255)), (5, 5))
        #nameSize = BRUSH.size(self.name)

        pygame.draw.rect(DISPLAYSURF, black, Rect((rx - 21 - my_player.position.x + 379,ry - 12 - my_player.position.y + 279 + 600),(78, 8)))
        global reloadclock
        if reloadclock > self.cachedreloadspeed - 1:
            reloadclock = self.cachedreloadspeed
        float(reloadclock)
        pygame.draw.rect(DISPLAYSURF, yellow, Rect((rx - 18 - my_player.position.x + 379,ry - 9 - my_player.position.y),(78*(float(self.timer/float(self.cachedreloadspeed))), 6)))

    def displayOther(self):
        rx = self.body.position.x
        print self.body.velocity
        ry = 600 - self.body.position.y
        xy = 600 - my_player.body.position.y
        #DISPLAYSURF.blit(PLAYERIMAGES[self.colour], (rx,ry))
        pygame.draw.rect(DISPLAYSURF, black, Rect((rx - 21 - my_player.body.position.x + 379,ry - 12 - 15 - xy + 279),(78, 8)))
        pygame.draw.rect(DISPLAYSURF, red, Rect((rx - 18 - my_player.body.position.x + 379,ry - 9 - 15 - xy + 279),(78, 6)))
        if self.health > 100:
            self.health = 100
        pygame.draw.rect(DISPLAYSURF, green, Rect((rx - 18 - my_player.body.position.x + 379,ry - 9 - 15 - xy + 279),(78*(self.health/100), 6)))
        nameSize = BRUSH.size(self.name)
        DISPLAYSURF.blit(self.cachedname, (rx + ((42 - nameSize[0])/2) - my_player.body.position.x + 379, ry - 33 - 20 - xy + 279))
        #DISPLAYSURF.blit(BRUSH.render(str(FPSCLOCK.get_fps()), True, (255,255,255)), (5, 5))
        #nameSize = BRUSH.size(self.name)

        pygame.draw.rect(DISPLAYSURF, black, Rect((rx - 21 - my_player.body.position.x + 379,ry - 12 - xy + 279),(78, 8)))
        #pygame.draw.rect(DISPLAYSURF, red, Rect((200,50),(78, 8)))
        if self.timer > self.cachedreloadspeed - 1:
            self.timer = self.cachedreloadspeed
        float(self.timer)
        timerbuffer = self.timer
        if timerbuffer > self.cachedreloadspeed:
            timerbuffer = self.cachedreloadspeed
        pygame.draw.rect(DISPLAYSURF, yellow, Rect((rx - 18 - my_player.body.position.x + 379,ry - 9 - xy + 279),(78*(float(timerbuffer/float(self.cachedreloadspeed))), 6)))

        if self.mx == False and self.body.velocity.x <= -0.7 and self.body.velocity.y <= 0.1:
            #ScientistLeft.blit(DISPLAYSURF, (379,279))
            #ScientistLeftRev.blit(DISPLAYSURF, (379,279))
            if self.displaypack == True:
                DISPLAYSURF.blit(IMAGESDICT['PackLeft'], (rx + 395 - my_player.body.position.x,ry + 272 - xy))
            PLAYERANIMS[self.colour]['Left'].blit(DISPLAYSURF, (rx + 379 - my_player.body.position.x,ry + 279 - xy))
            #if my_player.displayshoes == True:
            #    SpeedAnimLeft.blit(DISPLAYSURF, (381,279))
            #if my_player.displayshoes == True:
            #    ArmorAnimLeft.blit(DISPLAYSURF, (383,279))

        if self.mx == True and self.body.velocity.x >= 0.7 and self.body.velocity.y <= 0.1:
            #ScientistRight.blit(DISPLAYSURF, (379,279))
            if self.displaypack == True:
                DISPLAYSURF.blit(IMAGESDICT['PackRight'], (rx + 373 - my_player.body.position.x,ry + 272 - xy))
            PLAYERANIMS[self.colour]['Right'].blit(DISPLAYSURF, (rx + 379 - my_player.body.position.x,ry + 279 - xy))
            #if my_player.displayarmor == True:
            #    ArmorAnimRight.blit(DISPLAYSURF, (379,279))

        if self.mx == False and self.body.velocity.x >= 0.7 and self.body.velocity.y <= 0.1:
            #ScientistLeft.reverse()
            #ScientistLeftRev.blit(DISPLAYSURF, (379,279))
            if self.displaypack == True:
                DISPLAYSURF.blit(IMAGESDICT['PackLeft'], (rx + 395 - my_player.body.position.x,ry + 272 - xy))
            PLAYERANIMS[self.colour]['LeftRev'].blit(DISPLAYSURF, (rx + 379 - my_player.body.position.x,ry + 279 - xy))
            #if my_player.displayarmor == True:
            #    ArmorAnimLeft.blit(DISPLAYSURF, (383,279))

        if self.mx == True and self.body.velocity.x <= -0.7 and self.body.velocity.y <= 0.1:
            #ScientistRight.reverse()
            #ScientistRightRev.blit(DISPLAYSURF, (379,279))
            if self.displaypack == True:
                DISPLAYSURF.blit(IMAGESDICT['PackRight'], (rx + 373 - my_player.body.position.x,ry + 272 - xy))
            PLAYERANIMS[self.colour]['RightRev'].blit(DISPLAYSURF, (rx + 379 - my_player.body.position.x,ry + 279 - xy))
            #if my_player.displayarmor == True:
            #    ArmorAnimRight.blit(DISPLAYSURF, (379,279))

        if (self.body.velocity.y >= 1 and self.body.velocity!=0) or (self.body.velocity.x < 0.7 and self.body.velocity.x > -0.7):
            if self.mx == False:
                  if self.displaypack == True:
                      DISPLAYSURF.blit(IMAGESDICT['PackLeft'], (rx + 395 - my_player.body.position.x,ry + 272 - xy))
                  DISPLAYSURF.blit(PLAYERANIMS[self.colour]['LeftImmo'], (rx + 379 - my_player.body.position.x,ry + 279 - xy))
                  #if my_player.displayarmor == True:
                  #    DISPLAYSURF.blit(IMAGESDICT['ArmorLeft'], (385,279))
                  #if self.displayshoes == True:
                      #DISPLAYSURF.blit(IMAGESDICT['SpeedLeft'], (rx + 381 - my_player.body.position.x,ry + 308 - xy))
                  #PLAYERANIMS[my_player.colour]['LeftImmo'].blit(DISPLAYSURF, (379,279))
                  #ScientistLeft.blitFrameNum(0, DISPLAYSURF, (379,279))
            if self.mx == True:
                  if self.displaypack == True:
                      DISPLAYSURF.blit(IMAGESDICT['PackRight'], (rx + 373 - my_player.body.position.x,ry + 272 - xy))
                  DISPLAYSURF.blit(PLAYERANIMS[self.colour]['RightImmo'], (rx + 379 - my_player.body.position.x,ry + 279 - xy))
                  #if my_player.displayarmor == True:
                  #    DISPLAYSURF.blit(IMAGESDICT['ArmorRight'], (382,279))
                  #if self.displayshoes == True:
                      #DISPLAYSURF.blit(IMAGESDICT['SpeedRight'], (rx + 379 - my_player.body.position.x,ry + 308 - xy))
                  #PLAYERANIMS[my_player.colour]['RightImmo'].blit(DISPLAYSURF, (379,279))
                  #ScientistRight.blitFrameNum(10, DISPLAYSURF, (379,279))

        if self.mx == False:
            #DISPLAYSURF.blit(ScientistLeftImmo, (379,279))
            #ScientistLeft.blitFrameNum(0, DISPLAYSURF, (379,279))
            Gun2 = rot_center(GunReverse, math.degrees(math.atan(self.a)))
            if self.displayarmor == True:
                DISPLAYSURF.blit(IMAGESDICT['ArmorLeft'], (rx + 385- my_player.body.position.x,ry + 279 - xy))
            DISPLAYSURF.blit(Gun2, (rx + 379 - my_player.body.position.x,ry+285 - xy))

        if self.mx == True:
            Gun2 = rot_center(Gun, math.degrees(math.atan(self.a)))
            if self.displayarmor == True:
                DISPLAYSURF.blit(IMAGESDICT['ArmorRight'], (rx + 382 - my_player.body.position.x,ry + 279 - xy))
            #Gun2 = pygame.transform.rotate(Gun, math.degrees(math.atan(float((300 - my)) / float((mx - 400)))))
            DISPLAYSURF.blit(Gun2, (rx + 379 - my_player.body.position.x,ry + 285 - xy))
            #ScientistRight.blitFrameNum(10, DISPLAYSURF, (379,279))

    def move(self):
        #print self.body.position
        if self.body.velocity.y > 700:
            self.body.velocity.y = 700
        if self.body.velocity.x > 600:
            self.body.velocity.x = 600
        if self.body.velocity.x < -600:
            self.body.velocity.x = -600
        if self.body.position.y < -my_map.lowest_y+600 - 700:
            self.DieNow()
            self.inAir = False
        self.body.velocity.x *= 0.95

    def DieNow(self):
        SOUNDSDICT['Dead'].play()
        self.health = 100
        spawnpoint = my_map.spawns[random.randint(0, len(my_map.spawns)-1)]
        self.body.position = from_pygame(Vec2d(spawnpoint.position_x+65, spawnpoint.position_y+65), DISPLAYSURF)
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
        self.a = a
        self.mx = mx
        if mx >= 400:
            self.angle = math.atan(self.a)
            #print self.angle
            self.body.lol = Vec2d(parent.cachedvelocity, 0)
            self.body.apply_impulse((self.body.lol.rotated(self.angle)*20)+(parent.body.velocity/2))
        if mx < 400:
            self.angle = math.atan(self.a)
            #print self.angle
            self.body.lol = Vec2d(-parent.cachedvelocity, 0)
            self.body.apply_impulse((self.body.lol.rotated(self.angle)*20)+(parent.body.velocity/2))
        #self.shape.group = 1
        self.shape.sensor = True
        #self.body.angle_degrees = self.angle
        RocketList.append(self)

    def DisplayRocket(self):
        self.body.apply_force(self.body.mass*space.gravity*-1)
        if -100 < self.body.position.x - my_player.body.position.x + 379< 900 and -100 < self.body.position.y - my_player.body.position.y + 321< 700:
            BULLETS[self.parent.colour].blit(DISPLAYSURF, to_pygame((self.body.position.x-my_player.body.position.x+379, self.body.position.y-my_player.body.position.y+300), DISPLAYSURF))
        #self.trail = pymunk.Segment(self.body, self.oldpos, self.body.position, 16)
        #self.trail.sensor = True
        #pygame.draw.line(DISPLAYSURF, (255,255,255), to_pygame(self.oldpos, DISPLAYSURF), to_pygame(self.body.position, DISPLAYSURF), 6)
        #self.oldpos = self.body.position
        #if len(space.shape_query(self.shape)) > 1:
        #print space.segment_query_first(self.oldpos, self.body.position)
        #print self.body.position - self.oldpos
        if space.segment_query_first(self.oldpos, self.body.position) != None or len(space.shape_query(self.shape)) > 0:
            for i in space.shape_query(self.shape):
                if i in my_map.spawnlist:
                    print 'spawn ignored'
                elif i in my_map.poweruplist:
                    print 'pwup ignored'
                elif i not in my_map.spawnlist and i not in my_map.poweruplist:
                    #print space.shape_query(self.shape)
                    #print space.segment_query_first(self.oldpos, self.body.position)
                    self.ExploBlueCopy = EXPLOS[self.parent.colour].getCopy()
                    self.ExploBlueCopy.play()
                    self.ExploBlueCopy.loop = False
                    #if -100 < self.position.x - my_player.position.x < 900 and -100 < self.position.y - my_player.position.y < 700:
                    ExploAnimList.append((self.ExploBlueCopy,(to_pygame(self.body.position, DISPLAYSURF))))
                    SOUNDSDICT['Explosion'].play()
                    #RocketList.remove(self)
                    diff = my_player.body.position - self.body.position + Vec2d(5,15)
                    length = diff.length
                    direc = diff.normalized()
                    #direc *= 10.0/length*3000
                    lol =( 700 - length*9) * (my_player.damage + 15)/75 * 4
                    if lol < 0:
                        lol = 0
                    direc *= lol
                    #if direc.y > 700:
                        #direc.y = 700
                    my_player.body.apply_impulse(direc)
                    if self in RocketList:
                        RocketList.remove(self)
        self.oldpos = self.body.position.int_tuple


class OtherRocket:
    def __init__(self, parent, impulse, start_pos):
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
        self.body.apply_impulse(impulse)
        #self.shape.group = 1
        self.shape.sensor = True
        #self.body.angle_degrees = self.angle
        RocketList.append(self)

    def DisplayRocket(self):
        self.body.apply_force(self.body.mass*space.gravity*-1)
        if -100 < self.body.position.x - my_player.body.position.x + 379< 900 and -100 < self.body.position.y - my_player.body.position.y + 321< 700:
            BULLETS[self.parent.colour].blit(DISPLAYSURF, to_pygame((self.body.position.x-my_player.body.position.x+379, self.body.position.y-my_player.body.position.y+300), DISPLAYSURF))
        #self.trail = pymunk.Segment(self.body, self.oldpos, self.body.position, 16)
        #self.trail.sensor = True
        #pygame.draw.line(DISPLAYSURF, (255,255,255), to_pygame(self.oldpos, DISPLAYSURF), to_pygame(self.body.position, DISPLAYSURF), 6)
        #self.oldpos = self.body.position
        #if len(space.shape_query(self.shape)) > 1:
        #print space.segment_query_first(self.oldpos, self.body.position)
        #print self.body.position - self.oldpos
        if space.segment_query_first(self.oldpos, self.body.position) != None or len(space.shape_query(self.shape)) > 0:
            for i in space.shape_query(self.shape):
                if i in my_map.spawnlist:
                    print 'spawn ignored'
                elif i in my_map.poweruplist:
                    print 'pwup ignored'
                elif i not in my_map.spawnlist and i not in my_map.poweruplist:
                    #print space.shape_query(self.shape)
                    #print space.segment_query_first(self.oldpos, self.body.position)
                    self.ExploBlueCopy = EXPLOS[self.parent.colour].getCopy()
                    self.ExploBlueCopy.play()
                    self.ExploBlueCopy.loop = False
                    #if -100 < self.position.x - my_player.position.x < 900 and -100 < self.position.y - my_player.position.y < 700:
                    ExploAnimList.append((self.ExploBlueCopy,(to_pygame(self.body.position, DISPLAYSURF))))
                    SOUNDSDICT['Explosion'].play()
                    #RocketList.remove(self)
                    diff = my_player.body.position - self.body.position + Vec2d(5,15)
                    length = diff.length
                    direc = diff.normalized()
                    #direc *= 10.0/length*3000
                    lol =( 700 - length*9) * (my_player.damage + 15)/75 * 4
                    if lol < 0:
                        lol = 0
                    direc *= lol
                    #if direc.y > 700:
                        #direc.y = 700
                    my_player.body.apply_impulse(direc)
                    if self in RocketList:
                        RocketList.remove(self)
        self.oldpos = self.body.position.int_tuple

def rot_center(image, angle):
    """rotate an image while keeping its center and size"""
    orig_rect = image.get_rect()
    rot_image = pygame.transform.rotate(image, angle)
    rot_rect = orig_rect.copy()
    rot_rect.center = rot_image.get_rect().center
    rot_image = rot_image.subsurface(rot_rect).copy()
    return rot_image

    # or return tuple: (Surface, Rect)
        # return rot_image, rot_image.get_rect()

def rot_center_uneven(image, rect, angle):
        """rotate an image while keeping its center"""
        rot_image = pygame.transform.rotate(image, angle)
        rot_rect = rot_image.get_rect(center=rect.center)
        return rot_image

def AnimateCursor():
    global rotationCounter, scalingCounter, value
    IMAGESDICT['Crosshair'] = rot_center(pygame.image.load(os.path.join(mypath, 'Images', 'Cross.png')), rotationCounter)
    IMAGESDICT['Crosshair'] = pygame.transform.scale(IMAGESDICT['Crosshair'], (64-int(scalingCounter), 64-int(scalingCounter)))
    DISPLAYSURF.blit(IMAGESDICT['Crosshair'], (mx-((64-int(scalingCounter))/2),my-((64-int(scalingCounter))/2)))
    IMAGESDICT['Crosshair'] = IMAGESDICT['CrosshairC']
    rotationCounter -= 3
    if scalingCounter > 15:
        value = -0.6
    if scalingCounter < 1:
        value = 0.6
    scalingCounter += value

def get_key():
  #if shifttoggle == True:
    #pygame.key.set_mods(KMOD_SHIFT)
  #else:
    #pygame.key.set_mods(KMOD_NONE)
  while 1:
    #pygame.key.set_mods(KMOD_SHIFT)
    event = pygame.event.get()
    if len(event) > 0:
        #print event[0]
        if event[0].type == KEYDOWN:
            return event[0]
            #for x in event:
                #print chr(x.key)
            #print chr(event[0].unicode)
        else:
            return None

def ask():
    "ask(screen, question) -> answer"
    global chat
    global displaychat
    global shifttoggle
    pygame.font.init()
    current_string = []
    #print string.join(current_string,"")
    #while 1:
    inkey = get_key()
    if inkey != None:
        #current_string.append(inkey.encode('ascii','replace'))
        if inkey.key == K_LSHIFT or inkey == K_RSHIFT:
            shifttoggle = not shifttoggle
            #print 'toggled shift'
        if inkey.key == K_BACKSPACE:
            chat = chat[0:-1]
        elif inkey.key == K_RETURN:
            Chatmessage.id.value = my_player.id
            Chatmessage.msg.value = str(chat)
            Chatmessage.placeholder.value = random.randint(0, 255)
            client.send_reliable_message(Chatmessage)
            chat = '->'
        elif inkey.key == K_LCTRL:
            displaychat = False
        elif inkey == K_MINUS:
            current_string.append("_")
        elif inkey.key <= 127:
            current_string.append(inkey.unicode.encode('ascii','replace'))
            #current_string.append(chr(inkey))
        #print string.join(current_string,"")
        if len(chat) < 2:
            chat = '->'
        return string.join(current_string,"")
#Networking setup

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
        try:
            while self.connection:
                self.connection.update()
                time.sleep(0.0001)
        except (KeyboardInterrupt, SystemExit):
            #cleanup_stop_thread();
            sys.exit()

#Client-side messages

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
    'placeholder': 'string 5',
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

class MapInfo(legume.messages.BaseMessage):
    MessageTypeID = legume.messages.BASE_MESSAGETYPEID_USER+11
    MessageValues ={
    'name': 'string 30',
    'map': 'string 1300',
    'chunks': 'int',
    'chunk': 'int'
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

def custom_msghandler(sender, message):
        if message.MessageTypeID == MapInfo.MessageTypeID:
            global my_map
            global mapstring
            mapstring += message.map.value
            if message.chunk.value + 1 == message.chunks.value:
                my_map = Map(str(message.name.value), zlib.decompress(base64.b64decode(mapstring)))
                print 'Map received'
        if message.MessageTypeID == PlayerPositions.MessageTypeID:
            #playernamelist = pickle.loads(str(message.serializedplayerlist.value))
            msg = json.loads(str(message.serializedplayerpositions.value))
            for x in msg:
                ID, posx, posy, health, timer, a, mx, newbullet = x
                if ID == my_player.id:
                    my_player.health = health
                    my_player.body.position = Vec2d(posx, posy)
                    my_player.body.velocity = Vec2d(posx, posy) - my_player.oldvelocity
                    my_player.oldvelocity = Vec2d(posx, posy)
                else:
                    ID, otherplayers[ID].body.position.x, otherplayers[ID].body.position.y, otherplayers[ID].health, otherplayers[ID].timer, otherplayers[ID].a, otherplayers[ID].mx, newbullet = x
                    otherplayers[ID].body.velocity = Vec2d(posx, posy) - otherplayers[ID].oldvelocity
                    otherplayers[ID].oldvelocity = Vec2d(posx, posy)
                    #class OtherRocket:
                    #def __init__(self, parent, impulse, start_pos):
                    id, startpos, impulse = newbullet
                    if id != 0 and id != otherplayers[ID].alreadycreated:
                        rocket = OtherRocket(otherplayers[ID], Vec2d(impulse), Vec2d(startpos))
                        otherplayers[ID].alreadycreated = id
            #print playerpositions[0]
            #x = 0
            #for name in playernamelist:
            #    if name == my_player.name:
            #        my_player.body.position = Vec2d(playerpositions[x])
            #    x += 1
            #my_player.body.position = Vec2d(playerpositions[0])
            #print playerpositions[0]
        #if message.MessageTypeID == PlayerInfo.MessageTypeID:
        #    sx, sy = my_map.Spawns[random.randint(0, len(my_map.Spawns)-1)]
        #    clientplayer = Playerz(euclid.Vector2(sx, sy), message.colour.value, message.name.value, 100, euclid.Vector2(0, 0))
        #    IPRegistry[sender.address] = clientplayer
        #    PlayerList.append(clientplayer)
        #if message.MessageTypeID == DisconnectNotice.MessageTypeID:
        #    if sender in server.peers:
        #        PlayerList.remove(IPRegistry[sender.address])
        #        server.disconnect(sender.address)
        if message.MessageTypeID == IDmsg.MessageTypeID:
            my_player.id = message.id.value
        if message.MessageTypeID == DisconnectNotice.MessageTypeID:
            global space
            space.remove(otherplayers[message.id.value].body, otherplayers[message.id.value].shape)
            del otherplayers[message.id.value]
        if message.MessageTypeID == PlayerInfoServers.MessageTypeID:
            spawnpoint = my_map.spawns[random.randint(0, len(my_map.spawns)-1)]
            pos = Vec2d(spawnpoint.position_x+65, spawnpoint.position_y+65)
            newplayer = Playerz(from_pygame((spawnpoint.position_x+65, spawnpoint.position_y+65), DISPLAYSURF), message.colour.value, message.name.value, 100, euclid.Vector2(0, 0))

            newplayer.reloadspeed = message.reload.value
            newplayer.weaponvelocity = message.speedbullet.value
            newplayer.damage = message.damage.value
            newplayer.armor = message.armor.value
            newplayer.speed = message.speed.value
            newplayer.energy = message.energy.value

            newplayer.cacheddamage = 700 + newplayer.damage * 25
            newplayer.cachedvelocity = 15 + newplayer.weaponvelocity
            newplayer.cachedreloadspeed = 1500 - newplayer.reloadspeed * 50
            newplayer.cachedarmor = newplayer.armor * 0.03
            newplayer.cachedspeed = 1 + newplayer.speed * 0.1
            newplayer.cachedenergy = 0.1 + newplayer.energy * 0.1

            if newplayer.armor > 5:
                newplayer.displayarmor = True
            else:
                newplayer.displayarmor = False
            if newplayer.speed > 5:
                newplayer.displayshoes = True
            else:
                newplayer.displayshoes = False
            if newplayer.energy > 5:
                newplayer.displaypack = True
            else:
                newplayer.displaypack = False

            newplayer.ability = message.ability.value
            newplayer.id = message.id.value

            otherplayers[newplayer.id] = newplayer
        if message.MessageTypeID == Scoreboard.MessageTypeID:
            global allscores
            #print 'Score'
            allscores = json.loads(message.scores.value)
            #print allscores
        if message.MessageTypeID == Kills.MessageTypeID:
            killfeed.append(json.loads(message.kill.value))
            #print killfeed
        if message.MessageTypeID == ChatMsg.MessageTypeID:
            chathistory.append((message.id.value, message.msg.value, message.placeholder.value))
        if message.MessageTypeID == PwupStatus.MessageTypeID:
            if message.active.value == True:
                my_map.activepwups.append(my_map.powerups[message.id.value])
            else:
                my_map.activepwups.remove(my_map.powerups[message.id.value])
                ExploBlueCopy5 = Powerup.getCopy()
                ExploBlueCopy5.play()
                ExploBlueCopy5.loop = False
                #if -100 < self.position.x - my_player.position.x < 900 and -100 < self.position.y - my_player.position.y < 700:
                PowaList.append((ExploBlueCopy5,(to_pygame(my_map.powerups[message.id.value].body.position, DISPLAYSURF))))
                SOUNDSDICT['Powa'].play()

client = legume.Client()
#clientsettings = open(os.path.join(mypath, 'TXT files', 'ClientSettings.txt'), 'r')
#connectioninfo = clientsettings.readlines()

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


my_player = Playerz(euclid.Vector2(700,-300), 1, 'init', 100, euclid.Vector2(0,0))

ArrowStatuses = ArrowStatusMsg()
PlayerInfos = PlayerInfo()
DisconnectNotices = DisconnectNotice()
IDmsg = ID()
PlayerInfoServers = PlayerInfoServer()
Scores = ScoreboardRequest()
Chatmessage = ChatMsg()

Scores.placeholder.value = 'place'

int_ip = config['Connection']['server_ip'] #socket.gethostbyname(socket.getfqdn())
try:
    client.connect((int_ip, 6385))
except:
    client.connect(('192.168.1.4', 6385))
pygame.time.wait(75)

PlayerInfos.name.value = str(my_player.name)
PlayerInfos.colour.value = int(my_player.colour)
PlayerInfos.armor.value = int(my_player.armor)
PlayerInfos.speed.value = int(my_player.speed)
PlayerInfos.energy.value = int(my_player.energy)
PlayerInfos.damage.value = int(my_player.damage)
PlayerInfos.speedbullet.value = int(my_player.weaponvelocity)
PlayerInfos.reload.value = int(my_player.reloadspeed)
PlayerInfos.ability.value = str(my_player.ability)



#DisconnectNotices.name.value = str(my_player.name)

serverconnecttimecounter = 0

while client.connected != True and serverconnecttimecounter < 200:
    pygame.time.wait(100)
    client.update()
    serverconnecttimecounter += 1
    if serverconnecttimecounter == 200:
        print 'Could not connect to server after 20 seconds'

t1 = FetchUrls(client)
t1.start()

client.OnMessage += custom_msghandler

client.send_reliable_message(PlayerInfos)

while my_map == None:
    pygame.time.wait(1)
    client.update()
    print 'Waiting for map'

sentmsg = True

##Bot stuff
##global NamesText, NameLines, botnamebuffer
#BotOptions = open(os.path.join(mypath, 'TXT Files', 'Bot setup.txt'), 'r')
#BotOptionsLines = BotOptions.readlines()
#
#NamesText = open(os.path.join(mypath, 'TXT Files', 'Bot names.txt'), 'r')
#NameLines = NamesText.readlines()
#
#i = 0
#while int(BotOptionsLines[0]) > i:
#    botnamebuffer = random.randint(0, len(NameLines) - 1)
#    spawn = my_map.spawns[random.randint(0, len(my_map.spawns)-1)]
#    sx = spawn.position_x
#    sy = spawn.position_y
#    player = Playerz(euclid.Vector2(sx, sy), random.randint(0, 3), 'Bot', 100, euclid.Vector2(0,0))
#    #player.colour = random.randint(0, 3)
#    player.name = NameLines[botnamebuffer].strip()
#    if player.colour == 0:
#        #self.cachedname = BRUSH.render(INFO[0].replace("\n", ""), True, (153,204,0))
#        player.cachedname = textOutline(BRUSH, player.name, (153,204,0),(0,0,2))
#    if player.colour == 1:
#        #self.cachedname = BRUSH.render(INFO[0].replace("\n", ""), True, (94,165,199))
#        player.cachedname = textOutline(BRUSH, player.name, (94,165,199),(0,0,2))
#    if player.colour == 2:
#        #self.cachedname = BRUSH.render(INFO[0].replace("\n", ""), True, (191,59,42))
#        player.cachedname = textOutline(BRUSH, player.name, (191,59,42),(0,0,2))
#    if player.colour == 3:
#        #self.cachedname = BRUSH.render(INFO[0].replace("\n", ""), True, (255,255,0))
#        player.cachedname = textOutline(BRUSH, player.name, (255,255,0),(0,0,2))
#
#    #player.cachedname = BRUSH.render(NameLines[botnamebuffer].strip(), True, (153,204,0))
#    del NameLines[botnamebuffer]
#    i += 1
#    BotsList.append(player)



while running:  # main game loop
    #client.update()

    try:
        moving = False
        mx,my = pygame.mouse.get_pos()
        if my == None:
            my = 301
        if mx == None:
            mx = 401
        if my == 300:
            my = 301
        if mx == 400:
            mx = 401
        if mx >= 400:
            ArrowStatuses.mx.value = True
        else:
            ArrowStatuses.mx.value = False
        my_player.a = float((300 - my)) / float((mx - 400))
    
        if leftReleased == False:
            pygame.event.post(ghostleft)
            leftReleased = True
    
        if rightReleased == False:
            pygame.event.post(ghostright)
            rightReleased = True
    
        for event in pygame.event.get():
             if event.type == SONGFINISHED:
                  pygame.mixer.music.load(os.path.join(mypath, 'Tracks', random.choice(os.listdir(os.path.join(mypath, 'Tracks')))))
                  pygame.mixer.music.play()
                  pygame.mixer.music.set_endevent(SONGFINISHED)
                  pygame.mixer.music.set_volume(0.7 * MusicVolume/100)
             if event.type == USEREVENT+3:
                 reloaded = True
    
             if event.type == MOUSEBUTTONDOWN and event.button == 1 and displaychat == False:
                ArrowStatus[3] = '1'
    
             if event.type == MOUSEBUTTONDOWN and event.button == 1 and my_player.timer > my_player.cachedreloadspeed and displaychat == False:
                 my_player.shoot = True
                 SOUNDSDICT['Boom'].play()
                 my_player.timer = 0
                 ArrowStatus[3] = '1'
                 rocket = Rocket(my_player, my_player.a, mx, my_player.body.position)
                 reloaded = False
    
             #if event.type == MOUSEBUTTONDOWN and event.button == 3 and displaychat == False:
             #    my_player.abilitystatus = not my_player.abilitystatus
             #    if my_player.abilitystatus == True:
             #        Cloak2.play()
             #        Cloak2.prevFrame(Cloak2.elapsed % Cloak2.rate)
    
             if event.type == pygame.QUIT:
                client.send_reliable_message(DisconnectNotices)
                attempts = 0
                while client.connected == True:
                    try:
                        pygame.time.wait(100)
                        client.send_reliable_message(DisconnectNotices)
                        client.update()
                        client.disconnect()
                        attemps += 1
                        if attempts > 5:
                            sentmsg = True
                            running = False
                            t1._Thread__stop()
                            #t1.exit()
                            break
                    except:
                        attempts += 1
                        if attempts > 5:
                            sentmsg = True
                            running = False
                            t1._Thread__stop()
                            #t1.exit()
                            break
                sentmsg = True
                running = False
                t1._Thread__stop()
                #t1.exit()
    
             if event.type == KEYDOWN and event.key == K_ESCAPE:
                client.send_reliable_message(DisconnectNotices)
                attempts = 0
                while client.connected == True:
                    try:
                        pygame.time.wait(100)
                        client.send_reliable_message(DisconnectNotices)
                        client.update()
                        client.disconnect()
                        attempts += 1
                        if attempts > 5:
                            sentmsg = True
                            running = False
                            t1._Thread__stop()
                            #t1.exit()
                            break
                    except:
                        attempts += 1
                        if attempts > 5:
                            sentmsg = True
                            running = False
                            t1._Thread__stop()
                            #t1.exit()
                            break
                sentmsg = True
                running = False
                t1._Thread__stop()
                #t1.exit()
    
             if event == ghostright and displaychat == False:
                ArrowStatus[1] = '1'
                sentmsg = True
                my_player.body.velocity += (Vec2d(my_player.cachedspeed*30,0))
                if ghostinit == 1:
                    rightReleased = False
    
             if event == ghostleft and displaychat == False:
                 ArrowStatus[0] = '1'
                 sentmsg = True
                 my_player.body.apply_impulse(Vec2d(-my_player.cachedspeed*30,0))
                 if ghostinit == 1:
                     leftReleased = False
    
             if event.type == KEYDOWN and event.key == K_a and noLeft == False and displaychat == False:
                 if leftReleased == True:
                     if my_player.speeded == False:
                         my_player.body.apply_impulse(Vec2d(-my_player.cachedspeed*30,0))
                         ArrowStatus[0] = '1'
                         sentmsg = True
                     else:
                         my_player.body.velocity += (-my_player.cachedspeed*30-5,0)
                 leftReleased = False
    
             if event.type == KEYUP and event.key == K_a and displaychat == False:
                 ArrowStatus[0] = '0'
                 sentmsg = True
                 leftReleased = True
    
             if event.type == KEYDOWN and event.key == K_d and noRight == False and displaychat == False:
                 if rightReleased == True:
                     if my_player.speeded == False:
                         ArrowStatus[1] = '1'
                         sentmsg = True
                         my_player.body.velocity += (my_player.cachedspeed*30,0)
                     else:
                         my_player.body.velocity += (my_player.cachedspeed*30+5,0)
                 rightReleased = False
    
             if event.type == KEYUP and event.key == K_d and displaychat == False:
                 ArrowStatus[1] = '0'
                 sentmsg = True
                 rightReleased = True
    
             if event.type == KEYDOWN and event.key == K_w and displaychat == False:
                ArrowStatus[2] = '1'
    
             if event.type == KEYDOWN and event.key == K_w and 0 <= my_player.body.velocity.y <= 0.01 and displaychat == False: #and my_player.inAir == False:
                 pygame.key.set_repeat()
                 my_player.body.velocity += (0,600)
                 ArrowStatus[2] = '1'
                 sentmsg = True
                 pygame.key.set_repeat(2, 8)
                 SOUNDSDICT['Jump'].play()
    
             if event.type == KEYDOWN and event.key == K_TAB and displaychat == False:
                 pygame.key.set_repeat()
                 client.send_reliable_message(Scores)
                 displayscores = not displayscores
                 pygame.key.set_repeat(2, 8)
             if event.type == KEYDOWN and event.key == K_LCTRL:
                 pygame.key.set_repeat()
                 displaychat = not displaychat
                 if displaychat == True:
                     pygame.key.set_repeat(100, 50)
                 else:
                     pygame.key.set_repeat(2, 8)
                 #pygame.key.set_repeat(2, 8)
    
        ArrowStatuses.arrows.value = str("".join(ArrowStatus))
        ArrowStatuses.gunorientation.value = my_player.a
        #ArrowStatuses.shoot.value = my_player.shoot
        ArrowStatuses.ability.value = my_player.abilitystatus
    
        ArrowStatus[2] = '0'
        ArrowStatus[3] = '0'
    
        if client.connected:
            #DISPLAYSURF.blit(textOutline(BRUSH, str(client.latency), (255,255,255),(0,0,2)), (5, 30))
            client.send_message(ArrowStatuses)
    
        reloadclock += FPSCLOCK.get_time()
    
        dtime_ms = FPSCLOCK.tick(50)
        dtime = dtime_ms/1000
        dfps = 50/(FPSCLOCK.get_fps() + 0.001)
        if dfps > 2:
            dfps = 2
    
        m = 0
        while m <= 800 // bckgroundwidth2 + 1:
            DISPLAYSURF.blit(bckground2, ((m)*bckgroundwidth2 - (my_player.body.position.x/3)%bckgroundwidth2,0))
            #Crosshairs.blit(DISPLAYSURF, (mx -50, my - 50))
            #IMAGESDICT['Background'].blit(DISPLAYSURF, ((m)*bckgroundwidth - (my_player.body.position.x/3)%bckgroundwidth,0))
            m += 1
    
        if animatebck == True:
            m = 0
            while m <= 800 // bckgroundwidth + 1:
                #DISPLAYSURF.blit(IMAGESDICT['Background'], ((m)*bckgroundwidth - (my_player.body.position.x/3)%bckgroundwidth,0))
                #Crosshairs.blit(DISPLAYSURF, (mx -50, my - 50))
                IMAGESDICT['Background'].blit(DISPLAYSURF, ((m)*bckgroundwidth - (my_player.body.position.x/3)%bckgroundwidth,0))
                m += 1
    
    
    
        my_player.move() # Update the player's position and velocity
        #
        #for clientplayer in otherplayers:
        #    DISPLAYSURF.blit(PLAYERIMAGES[clientplayer.colour], (clientplayer.position - my_player.position + euclid.Vector2(379, 279)))
    
        for s in my_map.activepwups:
            if s.pwup == 2:
                sx, sy = s.body.position.x + 51, s.position_y + 51
                px, py = to_pygame(my_player.body.position, DISPLAYSURF)
                #if -300 < sx - my_player.body.position.x < 900 and -100 < sy - my_player.body.position.y < 700:
                Shield.blit(DISPLAYSURF, (sx - px + 400, sy - py + 351))
    
            elif s.pwup == 1:
                sx, sy = s.position_x + 51, s.position_y + 51
                #sl.x += 51
                #sl.y += 51
                px, py = to_pygame(my_player.body.position, DISPLAYSURF)
                #if -300 < sx - my_player.body.position.x < 900 and -100 < sy - my_player.body.position.y < 700:
                Speed.blit(DISPLAYSURF, (sx - px + 400, sy - py + 351))
    
            elif s.pwup == 0:
                sx, sy = s.position_x + 51, s.position_y + 51
                px, py = to_pygame(my_player.body.position, DISPLAYSURF)
                #DISPLAYSURF.blit(IMAGESDICT['Health'], (sx - my_player.position.x, sy - my_player.position.y))
                #if -300 < sx - my_player.body.position.x < 900 and -100 < sy - my_player.body.position.y < 700:
                Health.blit(DISPLAYSURF, (sx - px + 400, sy - py + 351))
                #s.image.blit(DISPLAYSURF, (sx - px + 400, sy - py + 351))
                #healthcoll = pygame.Rect(sx - my_player.body.position.x - 16, sy - my_player.body.position.y - 16, 32, 32)
                #if healthcoll.colliderect(my_player.rect) and my_player.health != 100:
                #    SOUNDSDICT['Powa'].play()
                #    my_map.Healths.remove(s)
                #    my_map.PowerTimes.append((int(pygame.time.get_ticks()) + 60000, 'H'))
                #    pygame.time.set_timer(21, 60000)
                #    if my_player.health <= 75:
                #        my_player.health += 25
                #    else:
                #        my_player.health = 100
    
        for x in my_map.PowerTimes:
            time, power = x
            if time < int(pygame.time.get_ticks()):
                if power == 'D':
                    my_map.Shields.append(my_map.DeletedPowerD[0])
                    my_player.cachedarmor -= 0.4
                    my_player.shielded = False
                    my_map.PowerTimes.remove(x)
                if power == 'S':
                    my_map.Speeds.append(my_map.DeletedPowerS[0])
                    my_player.speedup = 1
                    my_player.speeded = False
                    my_map.PowerTimes.remove(x)
                if power == 'H':
                    my_map.Healths.append(my_map.DeletedPowerH[0])
                    my_map.PowerTimes.remove(x)
    
    
        if my_player.abilitystatus == True:
            halfheight = ABILITYDICT[my_player.ability].getRect().height/2
            if my_player.ability != 'Cloak':
                ABILITYDICT[my_player.ability].blit(DISPLAYSURF, (379 - halfheight + 21, 279 - halfheight + 21))
            else:
                ABILITYDICT[my_player.ability].blit(DISPLAYSURF, (379 - halfheight + 21, 279 - halfheight + 21))
            #halfheight = Cloak2.getRect().height/2
            #Cloak2.blit(DISPLAYSURF, (379 - halfheight + 21, 279 - halfheight + 21))
            #
            ##x,y = coord
            #Explo, coord = anim
            #x, y = coord
            ##Explo.play
            #Explo.blit(DISPLAYSURF, (x - my_player.position.x - 110, y - my_player.position.y - 125))
            #if Explo.isFinished() == True:
            #      ExploAnimList.remove(anim)
    
        for platform in my_map.platforms:
            plx, ply = to_pygame(platform.body.position, DISPLAYSURF)
            lolx, loly = to_pygame(my_player.body.position, DISPLAYSURF)
            if -300 < platform.position_x - (lolx) + 379 < 900 and -100 < platform.position_y - loly + 321 < 700:
                if platform.type == 1:
                    DISPLAYSURF.blit(platform.image, (plx - (lolx) + 379, ply - loly + 318))
                else:
                    DISPLAYSURF.blit(platform.image, (plx - (lolx) + 379, ply - loly + 321))
    
        #for platform in my_map.movingplatforms:
        #    platform.body.velocity = Vec2d(platform.lx * math.sin(platform.sx * platform.xxx + platform.ox), platform.ly * math.sin(platform.sy * platform.yyy + platform.oy))
        #    platform.body.position.x += platform.lx * math.sin(platform.sx * platform.xxx + platform.ox) #* dfps
        #    platform.body.position.y -= platform.ly * math.sin(platform.sy * platform.yyy + platform.oy)
        #    #platform.body.apply_impulse = Vec2d(platform.lx * math.sin(platform.sx * platform.xxx + platform.ox), platform.ly * math.sin(platform.sy * platform.yyy + platform.oy))
        #    platform.yyy += 1
        #    platform.xxx += 1
        #    platform.body.update_position(platform.body, 1/50)
        #    space.reindex_shape(platform.shape)
        #    #space.reindex_static()
    
        #pygame.draw.rect(DISPLAYSURF, black, Rect(0 - lolx,0 - loly - 500,my_map.max_limit_x, my_map.max_limit_y + 773 + 50), 5)
    
        ##PyIgnition particle effects
        #source.SetPos(pygame.mouse.get_pos())
        #if source.curframe % 50 == 0:
        #    source.ConsolidateKeyframes()
        #fire.Update()
        #fire.Redraw()
    
        my_player.display() # Display the player
    
        for player in otherplayers:
            otherplayers[player].move()
            otherplayers[player].displayOther()
    
    
        if mx <= 400 and ArrowStatus[0] == '1' and ArrowStatus[1] == '0' and my_player.body.velocity.y <= 0.1:
            #ScientistLeft.blit(DISPLAYSURF, (379,279))
            #ScientistLeftRev.blit(DISPLAYSURF, (379,279))
            if my_player.displaypack == True:
                DISPLAYSURF.blit(IMAGESDICT['PackLeft'], (395,272))
            PLAYERANIMS[my_player.colour]['Left'].blit(DISPLAYSURF, (379,279))
            #if my_player.displayshoes == True:
            #    SpeedAnimLeft.blit(DISPLAYSURF, (381,279))
            #if my_player.displayshoes == True:
            #    ArmorAnimLeft.blit(DISPLAYSURF, (383,279))
    
        if mx > 400 and ArrowStatus[1] == '1' and ArrowStatus[0] == '0' and my_player.body.velocity.y <= 0.1:
            #ScientistRight.blit(DISPLAYSURF, (379,279))
            if my_player.displaypack == True:
                DISPLAYSURF.blit(IMAGESDICT['PackRight'], (373,272))
            PLAYERANIMS[my_player.colour]['Right'].blit(DISPLAYSURF, (379,279))
            #if my_player.displayarmor == True:
            #    ArmorAnimRight.blit(DISPLAYSURF, (379,279))
    
        if mx <= 400 and ArrowStatus[0] == '0' and ArrowStatus[1] == '1' and my_player.body.velocity.y <= 0.1:
            #ScientistLeft.reverse()
            #ScientistLeftRev.blit(DISPLAYSURF, (379,279))
            if my_player.displaypack == True:
                DISPLAYSURF.blit(IMAGESDICT['PackLeft'], (395,272))
            PLAYERANIMS[my_player.colour]['LeftRev'].blit(DISPLAYSURF, (379,279))
            #if my_player.displayarmor == True:
            #    ArmorAnimLeft.blit(DISPLAYSURF, (383,279))
    
        if mx > 400 and ArrowStatus[1] == '0' and ArrowStatus[0] == '1' and my_player.body.velocity.y <= 0.1:
            #ScientistRight.reverse()
            #ScientistRightRev.blit(DISPLAYSURF, (379,279))
            if my_player.displaypack == True:
                DISPLAYSURF.blit(IMAGESDICT['PackRight'], (373,272))
            PLAYERANIMS[my_player.colour]['RightRev'].blit(DISPLAYSURF, (379,279))
            #if my_player.displayarmor == True:
            #    ArmorAnimRight.blit(DISPLAYSURF, (379,279))
    
        if (my_player.body.velocity.y >= 1 and my_player.body.velocity!=0) or (ArrowStatus[0] == '0' and ArrowStatus[1] == '0') or (ArrowStatus[0] == '1' and ArrowStatus[1] == '1'):
            if mx <= 400:
                  if my_player.displaypack == True:
                      DISPLAYSURF.blit(IMAGESDICT['PackLeft'], (395,272))
                  DISPLAYSURF.blit(PLAYERANIMS[my_player.colour]['LeftImmo'], (379,279))
                  #if my_player.displayarmor == True:
                  #    DISPLAYSURF.blit(IMAGESDICT['ArmorLeft'], (385,279))
                  #if my_player.displayshoes == True:
                      #DISPLAYSURF.blit(IMAGESDICT['SpeedLeft'], (381,308))
                  #PLAYERANIMS[my_player.colour]['LeftImmo'].blit(DISPLAYSURF, (379,279))
                  #ScientistLeft.blitFrameNum(0, DISPLAYSURF, (379,279))
            if mx > 400:
                  if my_player.displaypack == True:
                      DISPLAYSURF.blit(IMAGESDICT['PackRight'], (373,272))
                  DISPLAYSURF.blit(PLAYERANIMS[my_player.colour]['RightImmo'], (379,279))
                  #if my_player.displayarmor == True:
                  #    DISPLAYSURF.blit(IMAGESDICT['ArmorRight'], (382,279))
                  #if my_player.displayshoes == True:
                      #DISPLAYSURF.blit(IMAGESDICT['SpeedRight'], (379,308))
                  #PLAYERANIMS[my_player.colour]['RightImmo'].blit(DISPLAYSURF, (379,279))
                  #ScientistRight.blitFrameNum(10, DISPLAYSURF, (379,279))
    
        if mx <= 400:
            #DISPLAYSURF.blit(ScientistLeftImmo, (379,279))
            #ScientistLeft.blitFrameNum(0, DISPLAYSURF, (379,279))
            Gun2 = rot_center(GunReverse, math.degrees(math.atan(float((300 - my)) / float((mx - 400)))))
            if my_player.displayarmor == True:
                DISPLAYSURF.blit(IMAGESDICT['ArmorLeft'], (385,279))
            DISPLAYSURF.blit(Gun2, (379,285))
    
        if mx > 400:
            Gun2 = rot_center(Gun, math.degrees(math.atan(float((300 - my)) / float((mx - 400)))))
            if my_player.displayarmor == True:
                DISPLAYSURF.blit(IMAGESDICT['ArmorRight'], (382,279))
            #Gun2 = pygame.transform.rotate(Gun, math.degrees(math.atan(float((300 - my)) / float((mx - 400)))))
            DISPLAYSURF.blit(Gun2, (379,285))
            #ScientistRight.blitFrameNum(10, DISPLAYSURF, (379,279))
    
        for anim in ExploAnimList:
            #x,y = coord
            Explo, coord = anim
            x, y = coord
            Explo.loop = False
            #Explo.play
            Explo.blit(DISPLAYSURF, (Vec2d(x,y) - to_pygame(my_player.body.position, DISPLAYSURF) - Vec2d(125, 125) + Vec2d(400, 300)))
            if Explo.isFinished() == True:
                  ExploAnimList.remove(anim)
    
        for anim in PowaList:
            #x,y = coord
            Explo, coord = anim
            x, y = coord
            Explo.loop = False
            #Explo.play 126,119
            Explo.blit(DISPLAYSURF, (Vec2d(x,y) - to_pygame(my_player.body.position, DISPLAYSURF) - Vec2d(0, 0) + Vec2d(395, 350)))
            if Explo.isFinished() == True:
                PowaList.remove(anim)
    
        #for player in BotsList:
        #    player.velocity.y += player.gravity * dfps * 17
        #    player.timer += dtime_ms
        #    if player.timer > 1500:
        #        rocket = Rocket(player.position + euclid.Vector2(400 - 8, 300 - 11), euclid.Vector2(10, 10), 0, 0, player, False, player.velocity)
        #        player.timer = 0
        #    if player.health < 1:
        #        SOUNDSDICT['Kill'].play()
        #        player.health = 100
        #        sx, sy = my_map.Spawns[random.randint(0, len(my_map.Spawns)-1)]
        #        player.position = euclid.Vector2(sx, sy)
        #        player.armor = 1
        #        player.shielded = False
        #    if -100 < player.position.x - my_player.position.x + 379 < 900 and -100 < player.position.y - my_player.position.y + 279 < 700:
        #        pygame.draw.rect(DISPLAYSURF, red, Rect(player.position.x - my_player.position.x + 379, player.position.y - my_player.position.y + 279, 42, 42), 5)
        #        player.displayBot()
        #    player.move()
        #    player.velocity.x = -10
        #    #player.position.y += 0.04 * dfps
        #    #player.position.x += 10 #* dfps #* dtime * 17
        #    if player.position.x < 0:
        #        player.velocity.x = 10
        #    #print dtime
        #    #print dfps
        #    #player.move
        #    #print player.position.x
        #    player.AIrect.centerx = player.position.x - my_player.position.x + 400
        #    player.AIrect.centery =player.position.y - my_player.position.y + 300
        #    pygame.draw.rect(DISPLAYSURF, COLORS[player.colour], player.AIrect, 3)
            #if player.AIrect.left < 0:
            #player.velocity.x = -10
    
        #if my_player.shielded == True:
        #    DISPLAYSURF.blit(IMAGESDICT['Bubble'], (368,267))
        #if my_player.speeded == True:
        #    DISPLAYSURF.blit(IMAGESDICT['Chili'], (379,279))
    
        #for collisionbox in my_map.collisionboxes:
        #    xrect,yrect = collisionbox.topleft
        #    if xrect < my_player.position.x + 421  and xrect + 168 > my_player.position.x + 379:
        #        if collisionbox not in my_map.MovingPlatform and my_player.velocity.y >= 0 and yrect <= my_player.position.y + my_player.velocity.y + 321 and yrect >= my_player.position.y + 321:
        #            my_player.position.y = yrect - 321
        #            if my_player.isOn1 == True:
        #                my_player.position.y = yrect - 321
        #                my_player.isOn1 = False
        #            my_player.inAir = False
        #
        #            my_player.velocity.y = 0
        #
        #            my_player.gravity = 0
        #
        #            my_player.isOn1 = False
        #
        #        if my_player.velocity.y <= -1 and yrect >= my_player.position.y + my_player.velocity.y + 289 and yrect <= my_player.position.y + 321:# or platformrecttop.centery < 450:
        #            my_player.inAir = True
        #            my_player.velocity.y = 3
        #
        #        if collisionbox not in my_map.MovingPlatform and my_player.velocity.x < 0 and yrect < my_player.position.y + 321 and yrect > my_player.position.y + 289:
        #                my_player.velocity.x = 4
        #                noRight = True
        #                my_player.inAir = True
        #                my_player.isOn1 = False
        #        else:
        #            noRight = False
        #            noLeft = False
        #
        #        if collisionbox not in my_map.MovingPlatform and my_player.velocity.x > 0 and yrect < my_player.position.y + 321 and yrect > my_player.position.y + 289:
        #                my_player.velocity.x = -4
        #                noLeft = True
        #                my_player.inAir = True
        #                my_player.isOn1 = False
        #        else:
        #            noRight = False
        #            noLeft = False
    
    
        #n = 0
        #for platform in my_map.objects:
        #    lolx = my_player.position.x
        #    loly = my_player.position.y
        #    DISPLAYSURF.blit(platform.block, (platform.position_x - (lolx), platform.position_y - loly))
        #    if my_map.collisionboxes[n] in my_map.MovingPlatform:
        #        if -300 < platform.position_x - (lolx) < 900 and -100 < platform.position_y - loly < 700:
        #            DISPLAYSURF.blit(IMAGESDICT[PlatformMoving], (platform.position_x - (lolx), platform.position_y - loly))
        #    n += 1
        #
        #for x in my_map.MovingPlatform:
        #    indice, velocity_x, velocity_y, offset_y,length_x, length_y = x
        #    if -300 < my_map.objects[indice].position_x - (lolx) < 900 and -100 < my_map.objects[indice].position_y - loly < 700:
        #        DISPLAYSURF.blit(IMAGESDICT['MovingDanger'], (my_map.objects[indice].position_x - (lolx), my_map.objects[indice].position_y - loly))
        #    my_map.objects[indice].position_y += math.sin(float((lol)/length_y)) * int(velocity_y) * -1
        #    my_map.objects[indice].position_x += math.sin(float(float(lol) /length_x + float(offset_y)))  * int(velocity_x) * -1
        #    xrect, yrect = my_map.collisionboxes[indice].topleft
        #    my_map.collisionboxes[indice].topleft = (my_map.objects[indice].position_x, my_map.objects[indice].position_y)
        #    displayrect = my_map.collisionboxes[indice].move((-my_player.position.x, -my_player.position.y))
        #    if xrect < my_player.position.x + 421  and xrect + 168 > my_player.position.x + 379:
        #        if  my_player.velocity.y >= 0 and yrect <= my_player.position.y + my_player.velocity.y + 350 and yrect >= my_player.position.y + 300:
        #            #print 'Moving'
        #            my_player.position.y = yrect - 321 + math.sin(float((lol)/length_y)) * int(velocity_y) * -1
        #            my_player.velocity.x = math.sin(float(float(lol) /length_x + float(offset_y)))  * int(velocity_x) * -1
        #            if my_player.isOn1 == True:
        #                my_player.position.y = yrect - 321
        #                my_player.isOn1 = False
        #            my_player.inAir = False
        #
        #            my_player.velocity.y = 0
        #
        #            my_player.gravity = 0
        #
        #            my_player.isOn1 = False
        #            noRight = False
        #            noLeft = False
        #
        #
        #    lol = float(lol + 1)
        #
        #
        #
        #if my_player.inAir == False:
        #    my_player.gravity = 0
        #if my_player.inAir == True:
        #    my_player.gravity = 0.04
        #    my_player.velocity.y = my_player.velocity.y + my_player.gravity * dfps * 17
        for rocket in RocketList:
            rocket.DisplayRocket()
    
        Crosshairs.blit(DISPLAYSURF, (mx -50, my - 50))
    
        #global ID, playerscore, kills, dea
    
        y = 0
    
        for x in killfeed:
            if len(killfeed) > 4:
                killfeed.remove(killfeed[0])
            ID1, msg, ID2, placeholder = x
            #y = killfeed.index(x)
    
            try:
                killer = otherplayers[ID1].cachedname
            except:
                killer = my_player.cachedname
    
            try:
                victim = otherplayers[ID2].cachedname
            except:
                victim = my_player.cachedname
    
            killmsg = textOutline(BRUSH, str(msg), (white),(0,0,2))
            DISPLAYSURF.blit(killer, (800 - 5 - victim.get_width() - killmsg.get_width() - 5 - killer.get_width(),5+25*y))
            #killmsg = textOutline(BRUSH, str(msg), (white),(0,0,2))
            DISPLAYSURF.blit(killmsg, (800 - 5 - victim.get_width() - killmsg.get_width(), 5+25*y))
            DISPLAYSURF.blit(victim, (800 - victim.get_width(),5+25*y))
            y += 1
    
        if displaychat == True:
            if len(chathistory) > 5:
                chathistory.remove(chathistory[0])
            letter = ask()
            if letter != None:
                chat+=letter
                #print chat
            #chatdisplay = textOutline(BRUSH, str(chat), (white),(0,0,2))
            DISPLAYSURF.blit(textOutline(BRUSH, str(chat), (white),(0,0,2)), (5, 570))
            y = 0
            for x in chathistory:
                ID, msg, placeholder = x
                #print msg
                #y = chathistory.index(x)
    
                try:
                    name = otherplayers[ID1].cachedname
                except:
                    if ID == 0:
                        name = textOutline(BRUSH, 'SERVER', (white),(0,0,2))
                    else:
                        name = my_player.cachedname
    
                DISPLAYSURF.blit(name, (5, 545 - y*25))
                DISPLAYSURF.blit(textOutline(BRUSH, ': ' + str(msg[2:]), (white),(0,0,2)), (5 + name.get_width(),  545 - y*25))
                y += 1
    
        if displaychat == False:
            y = 0
            for x in chathistory:
                ID, msg, placeholder = x
                #print msg
                #y = chathistory.index(x)
    
                try:
                    name = otherplayers[ID1].cachedname
                except:
                    if ID == 0:
                        name = textOutline(BRUSH, 'SERVER', (white),(0,0,2))
                    else:
                        name = my_player.cachedname
    
                DISPLAYSURF.blit(name, (5, 570 - y*25))
                DISPLAYSURF.blit(textOutline(BRUSH, ': ' + str(msg[2:]), (white),(0,0,2)), (5 + name.get_width(),  570 - y*25))
                y += 1
    
    
        if displayscores == True:
            y = 0
            client.send_reliable_message(Scores)
            #global allscores
            #global my_player
            #print len(allscores)
            #print allscores
            for xd in allscores:
                ID, playerscore, kills, deaths = xd
                playerscore = int(playerscore)
                if ID == my_player.id:
                    player = my_player
                else:
                    player = otherplayers[ID]
                DISPLAYSURF.blit(textOutline(BRUSH, 'Map:', (white),(0,0,2)), (5, 55))
                DISPLAYSURF.blit(textOutline(BRUSH, str(my_map.mapname[0:-4]), (white),(0,0,2)), (50, 55))
                DISPLAYSURF.blit(player.cachedname, (5, 105+25*y))
                DISPLAYSURF.blit(textOutline(BRUSH, 'Name', (white),(0,0,2)), (5, 80))
                DISPLAYSURF.blit(textOutline(BRUSH, 'Score', (white),(0,0,2)), (200, 80))
                DISPLAYSURF.blit(textOutline(BRUSH, 'Kills/', (white),(0,0,2)), (290, 80))
                DISPLAYSURF.blit(textOutline(BRUSH, 'Deaths', (white),(0,0,2)), (380, 80))
                #DISPLAYSURF.blit(player.cachedname, (200, 50+20*y))
                if player.colour == 0:
                    DISPLAYSURF.blit(textOutline(BRUSH, str(playerscore), (153,204,0),(0,0,2)), (200, 105+25*y))
                    DISPLAYSURF.blit(textOutline(BRUSH, str(kills) + '/', (153,204,0),(0,0,2)), (290, 105+25*y))
                    DISPLAYSURF.blit(textOutline(BRUSH, str(deaths), (153,204,0),(0,0,2)), (380, 105+25*y))
                if player.colour == 1:
                    DISPLAYSURF.blit(textOutline(BRUSH, str(playerscore), (94,165,199),(0,0,2)), (200, 105+25*y))
                    DISPLAYSURF.blit(textOutline(BRUSH, str(kills) + '/', (94,165,199),(0,0,2)), (290, 105+25*y))
                    DISPLAYSURF.blit(textOutline(BRUSH, str(deaths), (94,165,199),(0,0,2)), (380, 105+25*y))
                if player.colour == 2:
                    DISPLAYSURF.blit(textOutline(BRUSH, str(playerscore), (191,59,42),(0,0,2)), (200, 105+25*y))
                    DISPLAYSURF.blit(textOutline(BRUSH, str(kills) + '/', (191,59,42),(0,0,2)), (290, 105+25*y))
                    DISPLAYSURF.blit(textOutline(BRUSH, str(deaths), (191,59,42),(0,0,2)), (380, 105+25*y))
                if player.colour == 3:
                    DISPLAYSURF.blit(textOutline(BRUSH, str(playerscore), (255,255,0),(0,0,2)), (200, 105+25*y))
                    DISPLAYSURF.blit(textOutline(BRUSH, str(kills) + '/', (255,255,0),(0,0,2)), (290, 105+25*y))
                    DISPLAYSURF.blit(textOutline(BRUSH, str(deaths), (255,255,0),(0,0,2)), (380, 105+25*y))
    
                #print ID, playerscore, kills, deaths
                y += 1
    
        rocket = 0
        ghostinit = 1
        #for rocket in RocketList:
        #    rocket.UpdateAll(my_player)
    
        if my_player.health < 1:
            my_player.DieNow()
    
    
    
        #ArrowStatuses.arrows.value = str("".join(ArrowStatus))
        #ArrowStatuses.gunorientation.value = my_player.a
        ##ArrowStatuses.shoot.value = my_player.shoot
        #ArrowStatuses.ability.value = my_player.abilitystatus
        #
        #ArrowStatus[2] = '0'
        #ArrowStatus[3] = '0'
        #
        if client.connected:
            DISPLAYSURF.blit(textOutline(BRUSH, str(int(client.latency)), (255,255,255),(0,0,2)), (5, 30))
        #    client.send_message(ArrowStatuses)
    
        my_player.shoot = False
        space.step(1/50.0)
        #draw_space(DISPLAYSURF, space)
        for rocket in RocketList:
            rocket.body.reset_forces()
        pygame.display.update() # Display all to the screen (yay!)
        #pygame.event.pump()
        #draw_space(DISPLAYSURF, space)

    except KeyboardInterrupt:
        # do nothing here
        running = False
        try:
            client.send_reliable_message(DisconnectNotices)
            client.disconnect()
        except:
            pass
        t1._Thread__stop()




