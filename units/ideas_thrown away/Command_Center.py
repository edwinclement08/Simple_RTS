__author__ = 'Edwin Clement'
import pygame
# import Defense_Tower
# import Generator
# import Helipad
# import Resource_Center
# import Artillery_Shop


pygame.init()
screen = pygame.display.set_mode((800,600))

class Command_Center:
    name = "Command_Center"
    type = "building"

    attacking = False
    attacking_power = 0
    range = 0
    speed = 0
    health = 1000

    idle = True
    destroyed = False

    image_file = "command_center.bmp"
    w = width = 3      # in tiles
    h = height = 3

    display_image = pygame.Surface((3*20, 3*20))

    # image data
    image = pygame.image.load(image_file).convert()
    px_image = pygame.PixelArray(image)
    print len(px_image)
    image_idle = []
    for t in [0,1,2,3]: # there are 4 tiles
        image_idle.append(px_image[t*60:t*60+59,0:59].make_surface())
    print image_idle
    image_working = []
    for t in [0,1,2]: # there are 3 tiles
        image_working.append(px_image[t*60:t*60+59,60+20:60+20 + 59].make_surface())
    image_destroyed = px_image[0:59,60:60+59].make_surface()
    selection_image = image_idle[0]

    time_last_updated = pygame.time.get_ticks()
    frame_no = 0

    selection_options = {
        # 'Resource_Center': Resource_Center.Resource_Center("", -1, -1).selection_image,
        # 'Artillery_Shop': Artillery_Shop.Artillery_Shop("", -1, -1).selection_image,
        # 'Helipad': Helipad.Helipad("", -1, -1).selection_image,
        # 'Generator': Generator.Generator("", -1,-1).selection_image,
        # 'Defense_Tower': Defense_Tower.Defense_Tower("", -1, -1).selection_image
    }


    def __init__(self,allegiance,x,y):
        # data about itself
        self.allegiance = allegiance
        self.position = x, y

    def increase_frame_no(self):
        if self.idle:
            if self.frame_no >= 3 :
                self.frame_no = 0
                return 0
            else:
                self.frame_no += 1
        else:
            if self.frame_no >= 2:
                self.frame_no = 0
                return 0
            else:
                self.frame_no += 1

    def update(self):
        if self.destroyed:
            self.display_image.blit(self.image_destroyed,(0,0))
        else:
            if pygame.time.get_ticks() - self.time_last_updated >= 300:
                self.increase_frame_no()
            if self.idle:
                self.display_image.blit(self.image_idle[self.frame_no],(0,0))
            else:
                self.display_image.blit(self.image_working[self.frame_no],(0,0))

    def got_hit(self,points):
        if self.health - points >= 0:
            self.destroyed = True
            self.health = 0
        else:
            self.health = self.health - points

    def do_selection_option(self,sel = None):
        pass

e = Command_Center("me",10,20)
for s in range(50):
    screen.fill((255,255,255))
    pygame.event.pump()
    e.update()
    screen.blit(pygame.transform.scale(e.display_image, (60*3, 60*3)),(s,0))
    pygame.display.update()
    pygame.time.delay(250)
    screen.fill((0,0,0))
pygame.display.update()

pygame.quit()
