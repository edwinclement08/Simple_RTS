__author__ = 'Edwin Clement'

import json
import pygame
import sys
from pygame.locals import *
import find_path
# sys.path[0:0] = ("units",)
# from unit_base import *


class unit_attacking:
    type = "unit"
    destroyed = False
    cost = 0  # will be override

    total_health = 0  # will be override

    attacking = False
    range = 0  # will be override
    time_last_fired = 0
    time_for_reload = 0  # will be override

    image_array = []
    directions = [[(x, y) for x in (-1, 0, 1)] for y in (-1, 0, 1)]
    directions = directions[0] + directions[1] + directions[2]

    cur_direction = (0, -1)
    moving = False
    move_path = []
    move_progress = 0  # in percent
    time_since_last_inc = 0
    speed = 200  # (ms) will be override
    dx, dy = 0, 0
    # time interval between moves

    w, h = 1, 1

    def __init__(self, allegiance, x, y):
        self.allegiance = allegiance
        self.position = [x, y]
        self.image_file = "units/" + self.image_file
        master_image = pygame.image.load(self.image_file).convert()

        px_image = pygame.PixelArray(master_image)

        self.images = {}
        w, h = self.w*20, self.h*20
        for s in self.directions:
            x, y = (s[0]+1)*w, (s[1]+1)*h
            self.images[s] = px_image[x:x+w, y:y+h].make_surface()
            self.images[s].set_colorkey((0, 128, 128))

        self.selection_image = pygame.transform.scale(self.images[self.cur_direction], (40, 40))
        self.display_image = self.images[self.cur_direction]

        self.fx, self.fy = 0, 0
        self.health = self.total_health
        self.update()

    def update(self):
        self.any_other_stuff()
        self.display_image = self.images[self.cur_direction]
        if self.moving:
            if self.move_path:
                if self.move_progress >= 100:
                    self.position[0] += self.cur_direction[0]
                    self.position[1] += self.cur_direction[1]
                    self.move_progress = 0
                    print self.position, self.cur_direction, self.dx, self.dy
                    self.dx, self.dy = 0, 0
                    self.cur_direction = self.move_path.pop(0)
                    self.time_since_last_inc = pygame.time.get_ticks()
                else:
                    if pygame.time.get_ticks() - self.time_since_last_inc >= self.speed:
                        move_per_20 = self.move_progress/100.0*(20.0)

                        self.dx, self.dy = self.cur_direction[0]*move_per_20, self.cur_direction[1]*move_per_20

                        if self.cur_direction[0] == 0:
                            self.dx = 0
                        if self.cur_direction[1] == 0:
                            self.dy = 0
                        self.move_progress += 1
                        self.time_since_last_inc = pygame.time.get_ticks()
            else:
                self.moving = False
                self.move_path = []
                self.move_progress = 0  # in percent
                self.time_since_last_inc = pygame.time.get_ticks()

    def move(self, tx, ty):
        self.moving = True
        self.move_path = fp.get_path((self.position[0], self.position[1]), (tx, ty))
        self.move_progress = 0  # in percent
        self.cur_direction = self.move_path.pop(0)
        print self.cur_direction

        self.time_since_last_inc = pygame.time.get_ticks()
        self.dx, self.dy = 0, 0

    def any_other_stuff(self):
        pass

    def got_hit(self, points):
        if self.health - points >= 0:
            self.health = self.health - points
        else:
            self.destroyed = True
            self.health = 0

    def do_selection_option(self, sel=None):
        pass

    def right_click_handle(self):
        pass


class Hovercraft(unit_attacking):
    cost = 400
    total_health = 500

    range = 5
    time_for_reload = 700
    speed = 10

    image_file = "Hovercraft.bmp"

    w, h = 1, 1


class Copter(unit_attacking):
    cost = 700
    total_health = 200

    range = 10
    time_for_reload = 700
    speed = 1

    image_file = "Copter.bmp"

    w, h = 1, 1


class Paladin(unit_attacking):
    cost = 400
    total_health = 500

    range = 10
    time_for_reload = 1000
    speed = 1

    image_file = "Paladin.bmp"

    w, h = 1, 1


class Mobile_Missile(unit_attacking):
    cost = 400
    total_health = 500

    range = 5
    time_for_reload = 1000
    speed = 1

    image_file = "Mobile_Missile.bmp"

    w, h = 1, 1


class Gattling_Gun(unit_attacking):
    cost = 400
    total_health = 500

    range = 8
    time_for_reload = 1000
    speed = 1

    image_file = "Gattling_Gun.bmp"

    w, h = 1, 1

# pygame.init()
# screen = pygame.display.set_mode((800, 600))
# screen.fill((255, 255, 255))
#
# # Mobile_Missile Copter Gattling_Gun Paladin Hovercraft
# cc1 = Copter("me", 15, 10)
# cc2 = Mobile_Missile("me", 20, 10)
# cc3 = Gattling_Gun("me", 10, 10)
# cc4 = Paladin("me", 12, 1)
# cc5 = Hovercraft("me", 19, 4)
#
# screen.blit(cc1.images[(1,1)],(0,0))
# screen.blit(cc2.images[(1,1)],(40,0))
# pygame.display.update()
# pygame.time.delay(2000)
#
# fp = find_path.AStar("hgrev")
# cc1.move(1, 12)
# cc2.move(1, 18)
# cc3.move(3, 15)
# cc4.move(16, 4)
# cc5.move(10, 9)
#
# grid = pygame.Surface((401, 401))
# grid.fill((255, 255, 255))
#
# for x in range(0, 420, 20):
#     pygame.draw.line(grid, (100, 100, 100), (x, 0), (x, 400), 1)
# for y in range(0, 420, 20):
#     pygame.draw.line(grid, (100, 100, 100), (0, y), (400, y), 1)
#
#
# while 1:
#     screen.fill((255, 255, 255))
#
#     for event in pygame.event.get():
#         if event.type is QUIT:
#             pygame.quit()
#     cc1.update()
#     cc2.update()
#     cc3.update()
#     cc4.update()
#     cc5.update()
#
#     screen.blit(grid, (0, 0))
#     screen.blit(cc1.display_image, (cc1.position[0]*20+cc1.dx, cc1.position[1]*10+cc1.dy))
#     screen.blit(cc2.display_image, (cc2.position[0]*20+cc2.dx, cc2.position[1]*20+cc2.dy))
#     screen.blit(cc3.display_image, (cc3.position[0]*20+cc3.dx, cc3.position[1]*20+cc3.dy))
#     screen.blit(cc4.display_image, (cc4.position[0]*20+cc4.dx, cc4.position[1]*20+cc4.dy))
#     screen.blit(cc5.display_image, (cc5.position[0]*20+cc5.dx, cc5.position[1]*20+cc5.dy))
#
#     pygame.display.update()
#
# pygame.quit()



########################################################################################################################
########################################################################################################################
########################################################################################################################
########################################################################################################################
########################################################################################################################
########################################################################################################################









