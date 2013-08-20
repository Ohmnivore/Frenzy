\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
\\READ THIS - VERY IMPORTANT LINKS AT THE BOTTOM + Instructions\\
\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
INSTRUCTIONS
This branch is the python source code, and is the most up to date at all times. 
There is also a Windows branch, but source is always better.

Current version - 0.8.4 (!Beta!)
                  2nd digit represents the version of the client program
                  3rd digit represents the version of the server program
                  As a player, you should try to keep up to date with the 2nd digit
                  As a server host, you should keep up to date with the 3rd digit

TODO - Redo powerups graphics

Python dependencies:
-*Python 2.7
-*PyGame 1.9.2
-Cmd2, but you can edit the import to run Cmd instead (Cmd is in the standard library)
-Kivy
-*Pymunk
-*ConfigObj
-requests
-pywin32 (if you're running a server on Windows)

*Starred dependencies are the ones required for the game client, the rest are optional features

Client.py - the game client
CLIENTCLI.py - the game menu
MapEditorGUI - launches the map editor 
MapTest.py - offline map tester
Server.py - the server
ClientSettings.cfg - game client settings (faster than using CLIENTCLI.py)
ServerSettings.cfg - not a lot of options yet, but the essential ones are there

Notes - Master server is ONLINE! at http://frenzyms.appspot.com/
        ...but I still need to implement permanent storing with the Google datastore
        The server can't change maps yet (annoying threading problems)
        On my LAN the ping is as low as 1ms. Average is around 5ms. Pretty sweet.
        Moving platforms do not move yet

NAT - If you happen to be behind a NAT, and want to host a server, then forward port 6385. 
      This is basicaly the same thing you would do for any other online game like TF2 and such.

Maps contains all the maps created with the map editor. To edit one it must be in that folder.
Backgrounds contains all the backgrounds. You can add your own, but it must be tileable
horizontaly and be 600px high. You can also add a spritesheet for an animated background. 
Server rotation contains the map rotation for the server.
Images, Effects, Fonts, Sounds, Tracks contain art assets that can be replaced, just use the
same format and name for any replacement. 
   _______________________
///        FRENZY         \\\
\\\vvvvvvvvvvvvvvvvvvvvvvv///

                     ___---___
                  .--         --.
                ./   ()      .-. \.
               /   o    .   (   )  \
              / .            '-'    \
             | ()    .  O         .  |
            |                         |
            |    o           ()       |
            |       .--.          O   |
             | .   |    |            |
              \    `.__.'    o   .  /
               \                   /
                `\  o    ()      /' 
                  `--___   ___--'
                        ---

Frenzy is an online multiplayer 2D platformer-shooter.
Yeah, it’s that cool. Written in Python using
PyGame, and Legume, it’s licensed under the
Creative Commons Attribution Non-Commercial
3.0 Unported license. It’s inspired by many 3D
shooters, mainly Tribes, Quake, early CoDs and my
imagination. I encourage people to expirement with
the source code and to expand the community. Like
all online games, it depends on an active user base.
Frenzy supports custom maps, fully customized servers,
custom player stats, and custom art skins and sound
skins.
It’s coming along. Beta release
is planned somewhere around summer 2013.
Useful links:
Master server (viewable in-browser)
http://frenzyms.appspot.com/
Official website – self-explanatory
http://lasthazard.ohmnivore.elementfx.com
This work is licensed under the Creative Commons Attribution-NonCommercial 3.0 Unported License.
To view a copy of this license, visit
http://creativecommons.org/licenses/by-nc/3.0/
My blog – a couple of posts about the game and stuff related
to robotics
http://www.ohmnivore.elementfx.com
Google group
https://groups.google.com/forum/?hl=en&fromgroups#!forum/frenzy-game
GitHub repository
https://github.com/Ohmnivore/Frenzy
