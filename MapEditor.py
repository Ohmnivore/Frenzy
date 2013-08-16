#!/usr/bin/env python2.7
# Last Hazard on the Moon (A 2D Online Myltiplayer Platformer Shooter for Android --- yeah, it's that cool)
# By Mark Beiline ohmnivore.elementfx.com
# Created with PyGame
from pygame.locals import *
import pygame._view
import pygame, os, sys, math
import random
import pickle
import pyganim
import spritesheet
import pygsheet
import threading
import socket
from configobj import ConfigObj

#parentdir = os.path.dirname(os.path.abspath(__file__))
parentdir = os.path.dirname(os.path.abspath(sys.argv[0]))
sys.path.insert(0,parentdir)
mypath = os.path.normpath(os.path.dirname(os.path.abspath(sys.argv[0])))

config = ConfigObj(os.path.join(mypath,'ClientSettings.cfg'))

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

viewx = 0
viewy = 0
zoom = 100
grid = False
currentblock = 0
numberblocks = 4
platforms = []
NOTINBOUND = True
dragging = False
dfps = 1
displaymoving = False

pygame.init()
pygame.font.init()
FPSCLOCK = pygame.time.Clock()

# Setting of the system icon
icon=pygame.image.load(os.path.join(mypath, 'Images', 'ICO.ico'))
#icon=pygame.image.load('ICO.ico')
pygame.display.set_icon(icon)

# Setting of the caption and global font
pygame.display.set_caption('Frenzy - Map editor')
BRUSH = pygame.font.Font(os.path.join(mypath, 'Fonts', 'ElectricCity.TTF'), 18)
FPSCLOCK = pygame.time.Clock()

# Surface object that is drawn to the actual computer screen
DISPLAYSURF = pygame.display.set_mode((WINWIDTH, WINHEIGHT))
DISPLAYSURF2 = pygame.display.set_mode((WINWIDTH, WINHEIGHT))
#DISPLAYSURF3 = pygame.display.set_mode((WINWIDTH, WINHEIGHT))

Crosshairs = pyganim.PygAnimation(pygsheet.spritesheet(os.path.join(mypath, 'Images', 'Crosshairs3.png')).load_strip((0,0,100,100), 8, colorkey = (204, 204, 204), time = 0.05))
Crosshairs.play()

Health = pyganim.PygAnimation(pygsheet.spritesheet(os.path.join(mypath, 'Images', 'HoloHealthSprite2.png')).load_strip((0,0,32,32), 7, colorkey = (0, 0, 0), time = 0.07))
Health.play()

Shield = pyganim.PygAnimation(pygsheet.spritesheet(os.path.join(mypath, 'Images', 'HoloBatterySprite.png')).load_strip((0,0,32,32), 7, colorkey = (0, 0, 0), time = 0.07))
Shield.play()

Speed = pyganim.PygAnimation(pygsheet.spritesheet(os.path.join(mypath, 'Images', 'HoloSpeedSprite.png')).load_strip((0,0,32,32), 7, colorkey = (0, 0, 0), time = 0.07))
Speed.play()

RectBlocks = spritesheet.spritesheet(os.path.join(mypath, 'Images', 'RectBlocks.png')).load_strip((0,0,171,22), 16, colorkey = (51, 51, 51))
SquareBlocks = spritesheet.spritesheet(os.path.join(mypath, 'Images', 'SquareBlocks.png')).load_strip((0,0,168,171), 16, colorkey = (51, 51, 51))

IMAGESDICT = {'MovingDanger' : pygame.image.load(os.path.join(mypath, 'Images', 'dangermoving.png')).convert(),
              'Background' : pygame.image.load(os.path.join(mypath, 'Backgrounds', config['Video']['background'])).convert(),
              'Nuclear' : pygame.image.load(os.path.join(mypath, 'Images', 'Nuclear.png')).convert_alpha(),
              'Bio-hazard' : pygame.image.load(os.path.join(mypath, 'Images', 'Bio-hazard.png')).convert_alpha(),
              'Shield' : pygame.image.load(os.path.join(mypath, 'Images', 'BatteryBlock.png')).convert_alpha(),
              'Speed' : pygame.image.load(os.path.join(mypath, 'Images', 'SpeedBlock.png')).convert_alpha(),
              'Health' : pygame.image.load(os.path.join(mypath, 'Images', 'HealthBlock.png')).convert_alpha()}

IMAGESDICT['MovingDanger'].set_colorkey((51,51,51))
bckgroundwidth = IMAGESDICT['Background'].get_width()

pygame.mixer.music.load(os.path.join(mypath, 'Tracks', random.choice(os.listdir(os.path.join(mypath, 'Tracks')))))
pygame.mixer.music.play()

SONGFINISHED = USEREVENT+25
pygame.mixer.music.set_endevent(SONGFINISHED)

MusicVolume = int(config['Audio']['music'])
pygame.mixer.music.set_volume(0.7 * MusicVolume/100)

# The variable that keeps the main loop running
running = True

# Set key repeat to repeatable
pygame.key.set_repeat(1, 8)

# Hide the cursor
pygame.mouse.set_visible(0)

HOST = '127.0.0.1'                 # Symbolic name meaning all available interfaces
PORT = 50007              # Arbitrary non-privileged port
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST, PORT))
sock.setblocking(0)
#sock.settimeout(1000)
#pygame.time.wait(2000)

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

class Platform:
    def __init__(self, position_x, position_y, variety, mode = 0):
        self.position_x = position_x
        self.position_y = position_y
        self.imagecopy = None
        self.transimagescale = None
        self.selected = False
        self.type = variety
        self.sortpwup = mode
        if self.type == 0:
            self.image = random.choice(RectBlocks)
            self.transimage = self.image.copy()
            self.transimage.set_alpha(125)
            self.bound = Rect(position_x, position_y, 168, 22)
            self.rect = self.bound.copy()
        elif self.type == 1:
            self.image = random.choice(SquareBlocks)
            self.transimage = self.image.copy()
            self.transimage.set_alpha(125)
            self.bound = Rect(position_x, position_y, 168, 168)
            self.rect = self.bound.copy()
        elif self.type == 2:
            self.positionxinit = self.position_x
            self.positionyinit = self.position_y
            self.image = IMAGESDICT['MovingDanger']
            self.transimage = self.image.copy()
            self.transimage.set_alpha(125)
            self.bound = Rect(position_x, position_y, 168, 25)
            self.rect = self.bound.copy()
            self.lengthy = 100
            self.offsetx = 0
            self.offsety = 0
            self.speedy = 0.1
            self.lengthx = 100
            self.speedx = 0.1
            self.xxx = 0
            self.yyy = 0
        elif self.type == 3:
            self.image = IMAGESDICT['Bio-hazard']
            if self.sortpwup == 0:
                self.image = IMAGESDICT['Bio-hazard']
            elif self.sortpwup == 1:
                self.image = IMAGESDICT['Nuclear']
            self.transimage = self.image.copy()
            self.transimage.set_alpha(125)
            self.bound = Rect(position_x, position_y, 168, 168)
            self.rect = self.bound.copy()
        elif self.type == 4:
            self.image = IMAGESDICT['Health']
            if self.sortpwup == 0:
                self.image = IMAGESDICT['Health']
            elif self.sortpwup == 1:
                self.image = IMAGESDICT['Speed']
            elif self.sortpwup == 2:
                self.image = IMAGESDICT['Shield']
            self.transimage = self.image.copy()
            self.transimage.set_alpha(125)
            self.bound = Rect(position_x, position_y, 168, 168)
            self.rect = self.bound.copy()
        self.imagecopy = self.image.copy()
        self.imagecopy = pygame.transform.scale(self.image, (self.image.get_width()*zoom/100, self.image.get_height()*zoom/100))

SampleBlocks = [Platform(0,0,0), Platform(0,0,1), Platform(0,0,2), Platform(0,0,3), Platform(0,0,4)]
MapNameText = textOutline(BRUSH, os.path.splitext(os.path.basename(os.path.join(mypath, 'Maps', config['Map']['map'])))[0], (white),(0,0,2))

if os.stat(os.path.join(mypath, 'Maps', config['Map']['map']))[6] != 0:
    Map = pickle.load(open(os.path.join(mypath, 'Maps', config['Map']['map']), 'r'))

try:
    for x in Map:
        #posx, posy, variety, mode = x
        posx = x[0]
        posy = x[1]
        variety = x[2]
        platform = Platform(posx, posy, variety, x[3])
        #platform.mode = x[3]
        #platform.sortpwup = x[3]
        if platform.type == 2:
            platform.lengthx = x[4]
            platform.lengthy = x[5]
            platform.speedx = x[6]
            platform.speedy = x[7]
            platform.offsetx = x[8]
            platform.offsety = x[9]
        platforms.append(platform)
except:
    pass

for platform in platforms:
    pygame.transform.scale(DISPLAYSURF2, (WINWIDTH*zoom/100, WINHEIGHT*zoom/100))
    platform.imagecopy = pygame.transform.scale(platform.image, (platform.image.get_width()*zoom/100, platform.image.get_height()*zoom/100))

while running:  # main game loop
    mx,my = pygame.mouse.get_pos()
    #conn, addr = s.accept()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sock.close()
            #server.disconnect_clients()
            #server.accepting_disallow()
            #server.disconnect()
            #client.disconnect()
            running = False

        if event.type == KEYDOWN and event.key == K_ESCAPE:
            #server.disconnect_clients()
            #server.accepting_disallow()
            #server.disconnect()
            sock.close()
            #client.disconnect()
            running = False

        if event.type == SONGFINISHED:
            pygame.mixer.music.load(os.path.join(mypath, 'Tracks', random.choice(os.listdir(os.path.join(mypath, 'Tracks')))))
            pygame.mixer.music.play()
            pygame.mixer.music.set_endevent(SONGFINISHED)
            pygame.mixer.music.set_volume(0.7 * MusicVolume/100)

        if event.type == KEYDOWN and event.key == K_RIGHT:
            viewx += 20*100/zoom

        if event.type == KEYDOWN and event.key == K_LEFT:
            viewx -= 20*100/zoom

        if event.type == KEYDOWN and event.key == K_UP:
            viewy -= 20*100/zoom

        if event.type == KEYDOWN and event.key == K_DOWN:
            viewy += 20*100/zoom

        if event.type == MOUSEBUTTONDOWN and event.button == 3:
            NOTINBOUND = True
            for platform in platforms:
                if platform.bound.collidepoint( viewx + mx*100/zoom,viewy + my  *100/zoom) == True:
                    if platform.selected == True:
                        dragging = True
                        NOTINBOUND = False
            if NOTINBOUND == True:
                currentblock += 1
                if currentblock > numberblocks:
                    currentblock = 0
            #Right mouse click
        if event.type == MOUSEBUTTONUP and event.button == 3:
            dragging = False

        if event.type == MOUSEBUTTONDOWN and event.button == 1:
            #Left mouse click
            NOTINBOUND = True
            for platform in platforms:
                pygame.transform.scale(DISPLAYSURF2, (WINWIDTH*zoom/100, WINHEIGHT*zoom/100))
                platform.imagecopy = pygame.transform.scale(platform.image, (platform.image.get_width()*zoom/100, platform.image.get_height()*zoom/100))
                if platform.bound.collidepoint((viewx) + mx*100/zoom,(viewy) + my  *100/zoom) == True:
                    for x in platforms:
                        #x.selected == True:
                        if x != platform:
                            x.selected = False
                    platform.selected = not platform.selected
                    #sock.send(str(platform.type))
                    if platform.selected == False:
                        sock.send(str(0))
                    else:
                        if platform.type == 4 or platform.type == 3:
                            sock.send(str(platform.type)+str(platform.sortpwup))
                        elif platform.type == 0 or platform.type == 1:
                            sock.send(str(platform.type))
                        elif platform.type == 2:
                            sock.send(str(platform.type) + pickle.dumps([platform.lengthx, platform.lengthy, platform.speedx, platform.speedy, platform.offsetx, platform.offsety]))
                    #EchoInstance.transport.write(str(platform.type))
                    #client.send('nuclear', 9)
                    NOTINBOUND = False
            if NOTINBOUND == True:
                if grid == False:
                    if currentblock == 0:
                        SampleBlocks[currentblock].image = random.choice(RectBlocks)
                        SampleBlocks[currentblock].transimage = SampleBlocks[currentblock].image.copy()
                        SampleBlocks[currentblock].transimage.set_alpha(125)
                    elif currentblock == 1:
                        SampleBlocks[currentblock].image = random.choice(SquareBlocks)
                        SampleBlocks[currentblock].transimage = SampleBlocks[currentblock].image.copy()
                        SampleBlocks[currentblock].transimage.set_alpha(125)
                    newblock = Platform(mx*100/zoom + viewx, my*100/zoom + viewy, currentblock)
                    platforms.append(newblock)
    
                elif grid == True:
                    if currentblock == 0:
                        SampleBlocks[currentblock].image = random.choice(RectBlocks)
                        SampleBlocks[currentblock].transimage = SampleBlocks[currentblock].image.copy()
                        SampleBlocks[currentblock].transimage.set_alpha(125)
                    elif currentblock == 1:
                        SampleBlocks[currentblock].image = random.choice(SquareBlocks)
                        SampleBlocks[currentblock].transimage = SampleBlocks[currentblock].image.copy()
                        SampleBlocks[currentblock].transimage.set_alpha(125)
                    newblock = Platform((mx*100/zoom + viewx) - (mx*100/zoom + viewx)%(168), (my*100/zoom + viewy) - (my*100/zoom + viewy)%(168), currentblock)
                    platforms.append(newblock)

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 5:
        #if event.type == KEYDOWN and event.key == K_a:
            #mouse view controls
            zoom -= 5
            if zoom < 5:
                zoom = 5
            for platform in platforms:
                pygame.transform.scale(DISPLAYSURF2, (WINWIDTH*zoom/100, WINHEIGHT*zoom/100))
                platform.imagecopy = pygame.transform.scale(platform.image, (platform.image.get_width()*zoom/100, platform.image.get_height()*zoom/100))

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 4:
        #if event.type == KEYDOWN and event.key == K_s:
            #mouse view controls
            zoom += 5
            if zoom > 100:
                zoom = 100
            for platform in platforms:
                pygame.transform.scale(DISPLAYSURF2, (WINWIDTH*zoom/100, WINHEIGHT*zoom/100))
                platform.imagecopy = pygame.transform.scale(platform.image, (platform.image.get_width()*zoom/100, platform.image.get_height()*zoom/100))

        #if event.type == KEYDOWN and event.key == K_f:
            #pygame.image.save(DISPLAYSURF2, 'mapscreen.png')
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 2:
            #mouse view controls
            pygame.key.set_repeat()
            grid = not grid
            pygame.key.set_repeat(1, 8)

        if event.type == pygame.KEYDOWN and event.key == K_BACKSPACE:
            #mouse view controls
            for platform in platforms:
                if platform.selected == True:
                    platforms.remove(platform)
                    sock.send(str(0))
        
        if event.type == pygame.KEYDOWN and event.key == K_SPACE:
            pygame.key.set_repeat()
            displaymoving = not displaymoving
            for platform in platforms:
                if platform.type == 2:
                    platform.position_x, platform.position_y = platform.positionxinit, platform.positionyinit
                    platform.yyy = 0
                    platform.xxx = 0
            pygame.key.set_repeat(1, 8)

    m = 0
    while m <= 800 // bckgroundwidth + 1:
        DISPLAYSURF.blit(IMAGESDICT['Background'], ((m)*bckgroundwidth - (viewx/3)%bckgroundwidth,0))
        m += 1

    for platform in platforms:
        #if -300 < platform.position_x - viewx < 900 and -100 < platform.position_y - viewy < 700:
        DISPLAYSURF2.blit(platform.imagecopy, ((platform.position_x - viewx)*zoom/100, (platform.position_y - viewy)*zoom/100))
        if platform.selected == True:
            platform.bound.left = platform.position_x
            platform.bound.top = platform.position_y
            #platform.bound.width = platform.image.get_width() * zoom/100
            #platform.bound.height = platform.image.get_height() * zoom/100
            platform.rect = platform.bound.copy()
            platform.rect.height = platform.image.get_height() * zoom/100
            platform.rect.width = platform.image.get_width() * zoom/100
            platform.rect.left = platform.bound.left*zoom/100 - viewx*zoom/100
            platform.rect.top = platform.bound.top*zoom/100 - viewy*zoom/100
            pygame.draw.rect(DISPLAYSURF2, red, platform.rect, 5)

    if grid == True:
        z = 0
        w = 0
        while z <= 800 // (168 * zoom/100) + 5:
            pygame.draw.line(DISPLAYSURF, (255, 255, 255, 10), ((z*168 - viewx%168)*zoom/100, 0), ((z*168 - viewx%168)*zoom/100, 600))
            z += 1

        while w <= 600 // (168 * zoom/100) + 5:
            pygame.draw.line(DISPLAYSURF, white, (0, (w*168 - viewy%168)*zoom/100), (800, (w*168 - viewy%168)*zoom/100))
            w += 1

        SampleBlocks[currentblock].transimagescale = pygame.transform.scale(SampleBlocks[currentblock].transimage, (SampleBlocks[currentblock].transimage.get_width()*zoom/100, SampleBlocks[currentblock].transimage.get_height()*zoom/100))
        #DISPLAYSURF.blit(SampleBlocks[currentblock].transimagescale, (mx*zoom/100 - ((mx*zoom/100+viewx*zoom/100)%(168*zoom/100)), my*zoom/100 - ((my*zoom/100+viewy*zoom/100)%(168*zoom/100))))
        #(mx*100/zoom + viewx) - (mx*100/zoom + viewx)%(168), (my*100/zoom + viewy) - (my*100/zoom + viewy)%(168)
        #DISPLAYSURF.blit(SampleBlocks[currentblock].transimagescale, (mx - (mx%(168*zoom/100)), my - (my%(168*zoom/100))))
        DISPLAYSURF.blit(SampleBlocks[currentblock].transimagescale, ((mx) - (mx+viewx*zoom/100)%(168*zoom/100), (my) - (my+viewy*zoom/100)%(168*zoom/100)))
    
    elif grid == False:
        SampleBlocks[currentblock].transimagescale = pygame.transform.scale(SampleBlocks[currentblock].transimage, (SampleBlocks[currentblock].transimage.get_width()*zoom/100, SampleBlocks[currentblock].transimage.get_height()*zoom/100))
        DISPLAYSURF.blit(SampleBlocks[currentblock].transimagescale, (mx, my))

    if displaymoving == True:
        for platform in platforms:
            if platform.type == 2:
                platform.position_x += platform.lengthx * math.sin(platform.speedx * platform.xxx + platform.offsetx) #* dfps
                platform.position_y += platform.lengthy * math.sin(platform.speedy * platform.yyy + platform.offsety) #* dfps
                platform.yyy += 1
                platform.xxx += 1

    if dragging == True:
        for platform in platforms:
            if platform.selected == True:
                #relx, rely = pygame.mouse.get_rel()
                if grid == False:
                    platform.position_x = mx * 100/zoom + viewx 
                    platform.position_y = my * 100/zoom + viewy
                if grid == True:
        #DISPLAYSURF.blit(SampleBlocks[currentblock].transimagescale, ((mx) - (mx+viewx*zoom/100)%(168*zoom/100), (my) - (my+viewy*zoom/100)%(168*zoom/100)))
                    #platform.position_x = (mx* 100/zoom) - (mx* 100/zoom+viewx)%(168* 100/zoom)
                    #platform.position_y = (my* 100/zoom) - (my* 100/zoom +viewy)%(168* 100/zoom)
                    platform.position_x = viewx - viewx%168 + (mx*100/zoom - (mx*100/zoom)%(168))
                    platform.position_y = viewy - viewy%168 + (my*100/zoom - (my*100/zoom)%(168))
                #platform.position_x += relx
                #platform.position_y += rely

    try:
        data = sock.recv(1024)
        if data == 'nuclear' or len(data) - 7 >= 2 and data.find('nuclear') >= 2:
            for platform in platforms:
                if platform.selected == True:
                    platform.sortpwup = 1
                    platform.image = IMAGESDICT['Nuclear']
                    platform.imagecopy = pygame.transform.scale(platform.image, (platform.image.get_width()*zoom/100, platform.image.get_height()*zoom/100))
                    platform.transimage = self.image.copy()
                    platform.transimage.set_alpha(125)
                    platform.imagecopy = pygame.transform.scale(platform.image, (platform.image.get_width()*zoom/100, platform.image.get_height()*zoom/100))
        if data == 'biohazard' or len(data) - 9 >= 2 and data.find('biohazard') >= 2:
            for platform in platforms:
                if platform.selected == True:
                    platform.sortpwup = 0
                    platform.image = IMAGESDICT['Bio-hazard']
                    platform.imagecopy = pygame.transform.scale(platform.image, (platform.image.get_width()*zoom/100, platform.image.get_height()*zoom/100))
                    platform.transimage = self.image.copy()
                    platform.transimage.set_alpha(125)
                    platform.imagecopy = pygame.transform.scale(platform.image, (platform.image.get_width()*zoom/100, platform.image.get_height()*zoom/100))
        if data == 'heal' or len(data) - 4 >= 2 and data.find('heal') >= 2:
            for platform in platforms:
                if platform.selected == True:
                    platform.sortpwup = 0
                    platform.image = IMAGESDICT['Health']
                    platform.imagecopy = pygame.transform.scale(platform.image, (platform.image.get_width()*zoom/100, platform.image.get_height()*zoom/100))
                    platform.transimage = self.image.copy()
                    platform.transimage.set_alpha(125)
                    pygame.transform.scale(DISPLAYSURF2, (WINWIDTH*zoom/100, WINHEIGHT*zoom/100))
                    platform.imagecopy = pygame.transform.scale(platform.image, (platform.image.get_width()*zoom/100, platform.image.get_height()*zoom/100))
                    platform.sortpwup = 0
                    print platform.sortpwup
        if data == 'speed' or len(data) - 5 >= 2 and data.find('speed') >= 2:
            for platform in platforms:
                if platform.selected == True:
                    platform.sortpwup = 1
                    platform.image = IMAGESDICT['Speed']
                    platform.imagecopy = pygame.transform.scale(platform.image, (platform.image.get_width()*zoom/100, platform.image.get_height()*zoom/100))
                    platform.transimage = self.image.copy()
                    platform.transimage.set_alpha(125)
                    pygame.transform.scale(DISPLAYSURF2, (WINWIDTH*zoom/100, WINHEIGHT*zoom/100))
                    platform.imagecopy = pygame.transform.scale(platform.image, (platform.image.get_width()*zoom/100, platform.image.get_height()*zoom/100))
                    platform.sortpwup = 1
                    print platform.sortpwup
        if data == 'shield' or len(data) - 6 >= 2 and data.find('shield') >= 2:
            for platform in platforms:
                if platform.selected == True:
                    platform.sortpwup = 2
                    platform.image = IMAGESDICT['Shield']
                    platform.imagecopy = pygame.transform.scale(platform.image, (platform.image.get_width()*zoom/100, platform.image.get_height()*zoom/100))
                    platform.transimage = self.image.copy()
                    platform.transimage.set_alpha(125)
                    pygame.transform.scale(DISPLAYSURF2, (WINWIDTH*zoom/100, WINHEIGHT*zoom/100))
                    platform.imagecopy = pygame.transform.scale(platform.image, (platform.image.get_width()*zoom/100, platform.image.get_height()*zoom/100))
                    platform.sortpwup = 2
                    print platform.sortpwup
        if data[0] == 'i':
            numbers = pickle.loads(data[1:])
            for platform in platforms:
                if platform.selected == True:
                    platform.lengthx = numbers[0]
                    platform.lengthy = numbers[1]
                    platform.speedx = numbers[2]
                    platform.speedy = numbers[3]
                    platform.offsetx = numbers[4]
                    platform.offsety = numbers[5]
                if platform.type == 2:
                    platform.xxx = 0
                    platform.yyy = 0
                    platform.position_x = platform.positionxinit
                    platform.position_y = platform.positionyinit
        if data == 'quit':
            ToSave = []
            for platform in platforms:
                if platform.type == 2:
                    abrigedform = [platform.positionxinit, platform.positionyinit, platform.type, platform.sortpwup, platform.lengthx, platform.lengthy, platform.speedx, platform.speedy, platform.offsetx, platform.offsety]
                elif platform.type == 3 or platform.type == 4:
                    abrigedform = [platform.position_x, platform.position_y, platform.type, platform.sortpwup]
                elif platform.type == 0 or platform.type == 1:
                    abrigedform = [platform.position_x, platform.position_y, platform.type, 0]
                ToSave.append(abrigedform)
                
            #Map.write(pickle.dumps(abrigedform))
            pickle.dump(ToSave, open(os.path.join(mypath, 'Maps', config['Map']['map']), 'w'))
            running = False
            sys.exit()
        if data == 'save':
            ToSave = []
            for platform in platforms:
                if platform.type == 2:
                    abrigedform = [platform.positionxinit, platform.positionyinit, platform.type, platform.sortpwup, platform.lengthx, platform.lengthy, platform.speedx, platform.speedy, platform.offsetx, platform.offsety]
                elif platform.type == 3 or platform.type == 4:
                    abrigedform = [platform.position_x, platform.position_y, platform.type, platform.sortpwup]
                    print platform.sortpwup
                elif platform.type == 0 or platform.type == 1:
                    abrigedform = [platform.position_x, platform.position_y, platform.type, 0]
                ToSave.append(abrigedform)
                
            #Map.write(pickle.dumps(abrigedform))
            #pickle.dump(ToSave, open(os.path.join(mypath, 'Maps', MapOptions[0]), 'w'))
            open(os.path.join(mypath, 'Maps', config['Map']['map']), 'w').write( pickle.dumps(ToSave))
            #running = False
            #sys.exit()
    except:
        pass
    #conn.sendall(data)

    FPSCLOCK.tick(50)
    dfps = 50/(FPSCLOCK.get_fps() + 0.001)
    if dfps > 2:
        dfps = 2

    DISPLAYSURF.blit(textOutline(BRUSH, str(int(FPSCLOCK.get_fps())), (white),(0,0,2)), (5, 5))
    DISPLAYSURF.blit(MapNameText, (50, 5))
    pygame.display.update() # Display all to the screen (yay!)