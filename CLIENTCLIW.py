#!/usr/bin/env python2.7
#from cmd2 import Cmd as cmd
import cmd2 as cmd
import os
import webbrowser
import subprocess
import sys
import random
import json
from configobj import ConfigObj
import requests

parentdir = os.path.dirname(os.path.abspath(sys.argv[0]))
sys.path.insert(0,parentdir)
mypath = os.path.normpath(os.path.dirname(os.path.abspath(sys.argv[0])))

config = ConfigObj(os.path.join(mypath,'ClientSettings.cfg'))

global masterserver
masterserver = None
ms_connected = False
servers = []

web = True
connect = True
custom = True
mapping = True
credit = True
setting = True

class CLI(cmd.Cmd):
    """Command line interface for FRENZY."""

    global web, connect, custom, mapping, credit, setting

    prompt = 'FRENZY:'
    
    intro = "\n*Welcome to the frenzy command line interface*\nType menu or help to get started\nUse menu, connect, setting, custom, map, web, and credit to get around\n"

    def save_config(self):
        cfg = ConfigObj(os.path.join(mypath,'ClientSettingsDefault.cfg'))
        cfg.merge(config)
        cfg.write(open(os.path.join(mypath,'ClientSettings.cfg'), 'wb'))

    def do_menu(self, line):
        "Returns to main menu"
        global web, connect, custom, mapping, credit, setting
        print '\nMain menu active.\nAvailable menus: connect, setting, edit, map, web, credit\n'
        web = True
        connect = True
        custom = True
        mapping = True
        credit = True
        setting = True

    Redirects = {
        'news': 'http://lasthazard.ohmnivore.elementfx.com/',
        'forums': 'http://lasthazard.ohmnivore.elementfx.com/forums/',
        'events': 'http://lasthazard.ohmnivore.elementfx.com/calendar/',
        'chat': 'http://lasthazard.ohmnivore.elementfx.com/chat-room/',
        'contact': 'http://lasthazard.ohmnivore.elementfx.com/contact/'
    }

    def RedirectToWebsite(self, directory):
        webbrowser.open(self.Redirects[directory], 2, True)

    def do_web(self, line):
        "Opens up the web menu"
        global web
        print '\nWeb menu active.\nAvailable commands: page\n'
        web = True

    def do_credit(self, line):
        "Opens up the credits menu"
        global credit
        print '\nCredits menu active.\nAvailable commands: list, read\n'
        credit = True

    def do_map(self, line):
        "Opens up the map menu"
        global mapping
        print '\nMap menu active.\nAvailable commands: create, edit, test, maps\n'
        mapping = True

    def do_setting(self, line):
        "Opens up the settings menu"
        global setting
        print '\nSettings menu active.\nAvailable commands: music_volume, effects_volume, background, backgrounds, restore_settings\n'
        setting = True

    def do_custom(self, line):
        "Opens up the customization menu"
        global custom
        print '\nCustomization menu active.\nAvailable commands: g_speed, g_dmg, g_reload, p_speed, p_armor, p_energy, p_color, p_ability, profile, rolldice, changename\n'
        custom = True

    def do_connect(self, line):
        "Opens up the connection menu"
        global connect
        print '\nConnection menu active.\nAvailable commands: ms_set, get_list, index_connect, direct_connect\n'
        connect = True

    def do_page(self, line):
        "Opens a webpage from the game's website. Choose amongst news, forums, events, chat, and contact."
        global web
        if web == True:
            try:
                self.RedirectToWebsite(str(line))
            except:
                print '\nNone-existant page requested. Choose amongst news, forums, events, chat, and contact.\n'

    creditlist = {
        "python": "Python is a popular general-purpose, high-level programming language whose design philosophy emphasizes code readability. Python's syntax allows programmers to express concepts in fewer lines of code than would be possible in languages such as C, and the language provides constructs intended to enable clear programs on both a small and large scale.\n\nPython supports multiple programming paradigms, including object-oriented, imperative and functional programming styles. It features a dynamic type system and automatic memory management and has a large and comprehensive standard library.\n\nLike other dynamic languages, Python is often used as a scripting language, but is also used in a wide range of non-scripting contexts. Using third-party tools, Python code can be packaged into standalone executable programs. Python interpreters are available for many operating systems.\n\nCPython, the reference implementation of Python, is free and open source software and has a community-based development model, as do nearly all of its alternative implementations. CPython is managed by the non-profit Python Software Foundation.",
        "pygame" : "Pygame is a set of Python modules designed for writing games. Pygame adds functionality on top of the excellent SDL library. This allows you to create fully featured games and multimedia programs in the python language. Pygame is highly portable and runs on nearly every platform and operating system. Pygame itself has been downloaded millions of times, and has had millions of visits to its website.\n\nPygame is free.\n\nReleased under the GPL License, you can create open source, free, freeware, shareware, and commercial games with it.",
        "pymunk" : "Pymunk is an easy-to-use pythonic 2d physics library that can be used whenever you need 2d rigid body physics from Python. Perfect when you need 2d physics in your game, demo or other application! It is built on top of the very nice 2d physics library Chipmunk.",
        "legume" : "Designed primarily for use in cross-platform game development, legume provides non-reliable, reliable and in-order transmission of messages via UDP. The focus behind the features and design of legume:\n\nCater for the networking requirements of a multiplayer game with as little boiler-plate code as possible.\n\nPeaceful co-existence with widely-used game development frameworks and libraries such as pygame and pyglet.\n\nDon't rely on third-party libraries or platform specific functionality.",
        "kivy" : "Kivy is an open source Python library for developing multitouch application software with a natural user interface (NUI). It can run on Android, iOS, Linux, MacOS X, and Windows. Distributed under the terms of the GNU Lesser General Public License, Kivy is free and open source software.\n\nKivy is the main framework developed by the Kivy organization, alongside Python for Android, Kivy iOS, and several other libraries meant to be used on all platforms. Recently, Kivy got a $5000 grant from the Python Software Foundation for porting it to Python 3.3. Kivy also supports the Raspberry Pi which was funded through Bountysource.",
        "pyganim" : "Pyganim (pronounced like pig and animation) is a Python module for Pygame that makes it easy to add sprite animations to your Pygame game programs. Pyganim works with Pythons 2 and 3.",
        "music_artists" : "I have used freemusicarchive.com to find some very nice chiptune music. These are the artists whom I'd like to thank for their wonderful music: Eric Skiff, Buskerdroid, Sycamore Drive, Computer Truck, and Marvelry Skimmer.\n\nA chiptune also known as chip music or 8-bit music, is synthesized electronic music produced (or emulated) by the sound chips of vintage computers, video game consoles, and arcade machines, as well as with other methods such as emulation. In the early 1980s, personal computers became less expensive and more accessible than they had previously been. This led to a proliferation of outdated personal computers and game consoles that had been abandoned by consumers as they upgraded to newer machines. They were in low demand by consumers as a whole, and not difficult to find, making them a highly accessible and affordable method of creating sound or art. While it has been a mostly underground genre, chiptune has had periods of moderate popularity in the 1980s and 21st century, and has influenced the development of electronic dance music.",
        "various_modules" : "I've used various other Python modules as well. Some are built into Python, some aren't.\n\nos, urllib2, socket, pickle, cpickle, socketServer, random, sys, math, traceback, threading, euclid, spritesheet, webbrowser, cmd, zlib, base64, socket, json, string, twisted, subprocess"
    }

    def do_list(self, line):
        "Lists all the stuff I give credit to for FRENZY"
        global credit
        if credit == True:
            for name in self.creditlist.keys():
                print '\n' + name + '\n'

    def do_read(self, line):
        "Get more info regarding the specified credit"
        global credit
        if credit == True:
            print '\n' + self.creditlist[line] + '\n'

    def do_test(self, line):
        "Launches the offline map tester to test the specified map"
        global mapping
        global config
        if mapping == True:
            config['Map']['map'] = line + '.txt'
            self.save_config()
            #try:
            #    #subprocess.Popen([os.path.join(mypath, 'Client.py')])
            #    #os.system('python ' + os.path.join(mypath, 'MapTest.py'))
            #except:
            #    print '\nCould not start the map tester application\n'
            subprocess.Popen([os.path.join(mypath, 'MapTest.exe')])

    def do_edit(self, line):
        "Launches the map editor to edit the specified map"
        global mapping
        global config
        if mapping == True:
            config['Map']['map'] = line + '.txt'
            self.save_config()
            #try:
            #    #subprocess.Popen([os.path.join(mypath, 'Client.py')])
            #    #os.popen('python ' + os.path.join(mypath, 'MapEditorGUI.py'))
            #    #os.system('python ' + os.path.join(mypath, 'MapEditorGUI.py'))
            #except:
            #    print '\nCould not start the map editor application\n'
            subprocess.Popen([os.path.join(mypath, 'MapEditorGUI.exe')])

    def do_create(self, line):
        "Creates a new empty map with the specified name"
        global mapping
        global mypath
        global config
        if mapping == True:
            config['Map']['map'] = line + '.txt'
            self.save_config()
            newmap = open(os.path.join(mypath, 'Maps', str(config['Map']['map'])), 'w')

    def do_maps(self, line):
        "Lists all maps in your 'Maps' directory"
        global mypath
        global mapping
        if mapping == True:
            f = []
            for (dirpath, dirnames, filenames) in os.walk(os.path.join(mypath, 'Maps')):
                f.extend(filenames)
                break
            for x in f:
                print '\n' + x[0:-4] + ' (' + x + ')' + '\n'

    def do_music_volume(self, line):
        "Sets in-game music volume. Enter a value between 0 and 100."
        global setting
        global config
        if setting == True:
            try:
                config['Audio']['music'] = int(line)
                self.save_config()
            except:
                print '\n' + line + ' is not a valid input\n'

    def do_effects_volume(self, line):
        "Sets in-game effects volume. Enter a value between 0 and 100."
        global setting
        global config
        if setting == True:
            try:
                config['Audio']['effects'] = int(line)
                self.save_config()
            except:
                print '\n' + line + ' is not a valid input\n'

    def do_background(self, line):
        "Sets in-game background. Enter the full name of an existing file in the 'Backgrounds' directory."
        global setting
        global config
        if setting == True:
            config['Video']['background'] = os.path.basename(line)
            self.save_config()

    def do_backgrounds(self, line):
        "Lists all backgrounds in your 'Backgrounds' directory"
        global setting
        global mypath
        if setting == True:
            f = []
            for (dirpath, dirnames, filenames) in os.walk(os.path.join(mypath, 'Backgrounds')):
                f.extend(filenames)
                break
            for x in f:
                print '\n' + x[0:-4] + ' (' + x + ')' + '\n'

    def do_restore_settings(self, line):
        "Restores the settings to their original values"
        global setting
        global config
        if setting == True:
            config['Audio']['music'] = 100
            config['Audio']['effects'] = 100
            config['Video']['background'] = 'space.png'
            self.save_config()

#g_speed, g_dmg, g_reload, p_speed, p_armor, p_energy, p_color, p_ability, profile, rolldice

    def do_g_speed(self, line):
        "Sets the points to invest into your player's blaster's projectile velocity.\nMust be a value between 0 and 15.\nRemember, you only have 15 points to spend amongst projectile velocity and damage, and blaster reload speed. Choose wisely!"
        global custom
        global config
        if custom == True:
            config['Player']['g_speed'] = int(line)
            self.save_config()

    def do_g_dmg(self, line):
        "Sets the points to invest into your player's blaster's projectile damage.\nMust be a value between 0 and 15.\nRemember, you only have 15 points to spend amongst projectile velocity and damage, and blaster reload speed. Choose wisely!"
        global custom
        global config
        if custom == True:
            config['Player']['g_dmg'] = int(line)
            self.save_config()

    def do_g_reload(self, line):
        "Sets the points to invest into your player's blaster's reload speed velocity.\nMust be a value between 0 and 15.\nRemember, you only have 15 points to spend amongst projectile velocity and damage, and blaster reload speed. Choose wisely!"
        global custom
        global config
        if custom == True:
            config['Player']['g_reload'] = int(line)
            self.save_config()

    def do_p_speed(self, line):
        "Sets the points to invest into your player's movement speed.\nMust be a value between 0 and 15.\nRemember, you only have 15 points to spend amongst player speed, armor, and energy recharge rate. Choose wisely!"
        global custom
        global config
        if custom == True:
            config['Player']['p_speed'] = int(line)
            self.save_config()

    def do_p_armor(self, line):
        "Sets the points to invest into your player's armor.\nMust be a value between 0 and 15.\nRemember, you only have 15 points to spend amongst player speed, armor, and energy recharge rate. Choose wisely!"
        global custom
        global config
        if custom == True:
            config['Player']['p_armor'] = int(line)
            self.save_config()

    def do_p_energy(self, line):
        "Sets the points to invest into your player's energy recharge rate.\nMust be a value between 0 and 15.\nRemember, you only have 15 points to spend amongst player speed, armor, and energy recharge rate. Choose wisely!"
        global custom
        global config
        if custom == True:
            config['Player']['p_energy'] = int(line)
            self.save_config()

    def do_p_color(self, line):
        "Sets the player's color. Choose between green, blue, red, and yellow. This is a preference indication only. In game modes with teams, this option will be overriden by your assigned team's color."
        global custom
        global config
        if custom == True:
            if line.lower() == 'green':
                config['Player']['color'] = 0
            elif line.lower() == 'blue':
                config['Player']['color'] = 1
            elif line.lower() == 'red':
                config['Player']['color'] = 2
            elif line.lower() == 'yellow':
                config['Player']['color'] = 3
            if line.lower() != 'green' and line.lower() != 'blue' and line.lower() != 'red' and line.lower() != 'yellow':
                print '\n' + line + ' is not a valid color\n'
            self.save_config()

    def do_p_ability(self, line):
        "Sets the players ability. Choose between cloak, heal, heart-beat, shield, and timezone."
        global custom
        global config
        if custom == True:
            if line.lower() != 'cloak' and line.lower() != 'heal' and line.lower() != 'heart-beat' and line.lower() != 'shield' and line.lower() != 'timezone':
                print '\n' + line + ' is not a valid ability\n'
            else:
                config['Player']['ability'] = line.lower()
            self.save_config()

    def do_profile(self, line):
        "Displays current player and blaster attributes, as well as the remaining points to spend."
        global custom
        global config
        if custom == True:
            g_speed = int(config['Player']['g_speed'])
            g_dmg = int(config['Player']['g_dmg'])
            g_reload = int(config['Player']['g_reload'])
            p_speed = int(config['Player']['p_speed'])
            p_armor = int(config['Player']['p_armor'])
            p_energy = int(config['Player']['p_energy'])
            if int(config['Player']['color']) == 0:
                color = 'Green'
            if int(config['Player']['color']) == 1:
                color = 'Blue'
            if int(config['Player']['color']) == 2:
                color = 'Red'
            if int(config['Player']['color']) == 3:
                color = 'Yellow'
            name = config['Player']['name']
            ability = config['Player']['ability']
    
            print '\n' + str(15 - p_speed - p_armor - p_energy) + ' player points remaining'
            print str(15 - g_speed - g_dmg - g_reload) + ' blaster points remaining\n'
            print 'Player attributes:'
            print 'Name: ' + name
            print 'Color: ' + color
            print 'Ability: ' + ability + '\n'
            print 'Speed: ' + str(p_speed)
            print 'Armor: ' + str(p_armor)
            print 'Energy: ' + str(p_energy) + '\n'
            print 'Blaster attributes:'
            print 'Speed: ' + str(g_speed)
            print 'Damage: ' + str(g_dmg)
            print 'Reload: ' + str(g_reload) + '\n'

    def do_rolldice(self, line):
        "Randomly sets the player and blaster attributes *(does not modify color or ability)*\nPretty cool if you just want to try out different playing styles."
        global custom
        global config
        if custom == True:
            g_speed = random.randint(0, 15)
            g_dmg = random.randint(0, 15 - g_speed)
            g_reload = 15 - g_speed - g_dmg
            p_speed = random.randint(0, 15)
            p_armor = random.randint(0, 15 - p_speed)
            p_energy = 15 - p_speed - p_armor

            config['Player']['g_speed'] = g_speed
            config['Player']['g_dmg'] = g_dmg
            config['Player']['g_reload'] = g_reload
            config['Player']['p_speed'] = p_speed
            config['Player']['p_armor'] = p_armor
            config['Player']['p_energy'] = p_energy

            print 'Player attributes:'
            print 'Speed: ' + str(p_speed)
            print 'Armor: ' + str(p_armor)
            print 'Energy: ' + str(p_energy) + '\n'
            print 'Blaster attributes:'
            print 'Speed: ' + str(g_speed)
            print 'Damage: ' + str(g_dmg)
            print 'Reload: ' + str(g_reload) + '\n'
            self.save_config()

    def do_changename(self, line):
        "Changes your player's name. There are a few rules here: max length is 16 letters. Also, no whitespace or characters that aren't in the US keyboard. Basicaly, numbers and latin characters without accents are fine."
        global config
        global custom
        if custom == True:
            if len(''.join(line.split())) > 0 and len(''.join(line.split())) == len(line) and len(line) <= 16:
                config['Player']['name'] = line
                self.save_config()
            else:
                print '\nInvalid name\n'
                print "There are a few rules here: max length is 16 characters. Also, no whitespace or characters that aren't in the US keyboard. Basicaly, numbers and latin characters without accents are fine.\n"

#masterserver_connect, get_list, number_connect, direct_connect

    def do_get_list(self, line):
        "Gets the server list from the masterserver."
        global connect
        global masterserver
        global ms_connected
        global servers
        if connect == True:
            if line == 'default':
                IP = config['Connection']['default_ms_ip']
            else:
                IP = line
            try:
                r = str(requests.get(str(IP)).text)
                #print r
                #    #print msg
                #    #try:
                print ''
                y = 0
                try:
                    servers = json.loads(r)
                    print '//////////////////////////////////////////////////////////////////'
                    print '/Index|Name|Mapname:Gamemode|Currentplayers/Maxplayers|Passworded/'
                    print '//////////////////////////////////////////////////////////////////'
                    print ''
                    for x in servers:
                        #name, mapname, gamemode, currentplayers, maxplayers, passw, serverip = x
                        print '%(name)s|%(mapname)s|%(gm)s|%(cp)d/%(mp)d|%(pass)s|%(ip)s' % \
                        {'name':str(x[0]),'mapname':str(x[1]),'gm':x[2],'cp':x[3],'mp':x[4],'pass':str(x[5]),'ip':x[6]}
                        #pprint((y, name, mapname, gamemode, currentplayers, '/', maxplayers, passw))
                        y += 1
                    print ''
                except:
                    print '\nThere are no public servers at the moment. Will YOU be daring enough to host one? Head to lasthazard.ohmnivore.elementfx.com for instructions.\n'
            except:
                print "\nWell heck, we can't get the server list. Either the master server is down, or your connection is the problem. Try visiting it from your browser.\n"
            #except:
                #print "\nWell heck, we can't get the server list. The connection to the master server must have been lost, or it's a firewall problem.\n"

    def do_index_connect(self, line):
        "Connects to the server corresponding to the index passed on the server list received from the master server."
        global connect
        global config
        global server
        global mypath
        if connect == True:
            try:
                config['Connection']['server_ip'] = servers[int(line)][6]
                try:
                    subprocess.Popen([os.path.join(mypath, 'Client.exe')])
                    #subprocess.Popen([os.path.join(mypath, 'Client.py')])
                    #os.popen('python ' + os.path.join(mypath, 'Client.py'))
                except:
                    print '\nCould not start the client application\n'
            except:
                print '\n' + line + ' is not a valid input. Either you have not yet fetched the server list from the masterserver, or the specified index is out of range.\n'

    def do_direct_connect(self, line):
        "Connects directly to the IP specified. Use this to resolve ugly NATs and LAN problems, or if the master server is down."
        global connect
        global config
        if connect == True:
            config['Connection']['server_ip'] = line
            try:
                #subprocess.Popen([os.path.join(mypath, 'Client.py')])
                subprocess.Popen([os.path.join(mypath, 'Client.exe')])
            except:
                print '\nCould not start the client application\n'

    def do_ms_set(self, line):
        "Sets the master server IP to use when passing the 'default' argument to the 'ms_connect' command."
        global connect
        global config
        if connect == True:
            config['Connection']['default_ms_ip'] = line

    def do_EOF(self, line):
        "Closes the FRENZY command line interface session"
        return True

    def do_shell(self, line):
        "Runs a shell command"
        print "running shell command:", line
        output = os.popen(line).read()
        print output
        self.last_output = output

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        CLI().onecmd(' '.join(sys.argv[1:]))
    else:
        CLI().cmdloop()