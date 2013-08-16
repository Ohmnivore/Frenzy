# This class handles sprite sheets
# This was taken from www.scriptefun.com/transcript-2-using
# sprite-sheets-and-drawing-the-background
# I've added some code to fail if the file wasn't found..
# Note: When calling images_at the rect is the format:
# (x, y, x + offset, y + offset)
 
import pygame, copy
 
class spritesheet(object):
    def __init__(self, filename):
        try:
            self.sheet = pygame.image.load(filename).convert()
        except pygame.error, message:
            print 'Unable to load spritesheet image:', filename
            raise SystemExit, message
    # Load a specific image from a specific rectangle
    def image_at(self, rectangle, colorkey = None, time = 0.1):
        "Loads image from x,y,x+offset,y+offset"
        rect = pygame.Rect(rectangle)
        image = pygame.Surface(rect.size).convert()
        image.blit(self.sheet, (0, 0), rect)
        if colorkey is not None:
            if colorkey is -1:
                colorkey = image.get_at((0,0))
            image.set_colorkey(colorkey, pygame.RLEACCEL)
        return (image, time)
    # Load a whole bunch of images and return them as a list
    def images_at(self, rects, colorkey = None, time = 0.1):
        "Loads multiple images, supply a list of coordinates" 
        return [self.image_at(rect, colorkey, time) for rect in rects]
    # Load a whole strip of images
    def load_strip(self, rect, image_count, colorkey = None, time = 0.1):
        "Loads a strip of images and returns them as a list"
        tups = [(rect[0]+rect[2]*x, rect[1], rect[2], rect[3])
                for x in range(image_count)]
        return self.images_at(tups, colorkey, time)

class spritesheetalpha(object):
    def __init__(self, filename):
        try:
            self.sheet = pygame.image.load(filename).convert_alpha()
        except pygame.error, message:
            print 'Unable to load spritesheet image:', filename
            raise SystemExit, message
    # Load a specific image from a specific rectangle
    def image_at(self, rectangle, colorkey = None, time = 0.1):
        "Loads image from x,y,x+offset,y+offset"
        rect = pygame.Rect(rectangle)
        image = pygame.Surface(rect.size,pygame.SRCALPHA, 32)
        image.convert_alpha()
        image.blit(self.sheet, (0, 0), rect)
        return (image, time)
    # Load a whole bunch of images and return them as a list
    def images_at(self, rects, colorkey = None, time = 0.1):
        "Loads multiple images, supply a list of coordinates" 
        return [self.image_at(rect, colorkey, time) for rect in rects]
    # Load a whole strip of images
    def load_strip(self, rect, image_count, colorkey = None, time = 0.1):
        "Loads a strip of images and returns them as a list"
        alltups = []
        tups = []
        #mergelist = []
        y = 0
        x = 0
        while y <= ((self.sheet.get_height() / rect[3]) - 1):
            while x < image_count:
                tups.append((rect[0]+rect[2] * x, rect[1] + y * rect[3], rect[2], rect[3]))
                x += 1
            y += 1
            x = 0
        return self.images_at(tups, colorkey, time)
#0,0,80 -> width, 80 -> height
