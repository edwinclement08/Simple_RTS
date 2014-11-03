__author__ = 'Edwin Clement'
import pygame
pygame.init()
pygame.display.set_mode((10,10))
class Command_Center:
    name = "Command_Center"

    attacking = False
    attacking_power = 0
    range = 0

    type = "building"
    speed = 0

    health = 1000

    w = width = 3      # in tiles
    h = height = 3

    idle = True
    destroyed = False
    image_file = "command_center.bmp"

    display_image = pygame.Surface((3*20, 3*20))

    def __init__(self,allegiance,x,y):
        self.allegiance = allegiance
        self.position = x, y

        # data about itself
        self.display_image = pygame.Surface((3*20, 3*20))

        # image data
        self.image = pygame.image.load(self.image_file).convert()
        self.px_image = pygame.PixelArray(self.image)
        self.image_idle = []
        for t in range(4): # there are 4 tiles
            self.image_idle.append(self.px_image[t*60:t*60+59,0:59].make_surface())
        print self.image_idle
        self.image_working = []
        for t in range(3): # there are 3 tiles
            self.image_working.append(self.px_image[t*60:t*60+59,60+20:60+20 + 59].make_surface())
        self.image_destroyed = self.px_image[0:59,120+40:120+40 + 59].make_surface()
        self.selection_image = self.image_idle[0]

        self.time_last_updated = pygame.time.get_ticks()
        self.frame_no = 0

s = Command_Center('',-1,-1)