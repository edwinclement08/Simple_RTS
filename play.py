__author__ = 'Edwin Clement'

import pygame
import sys
sys.path[0:0] = ("units",)
from pygame.locals import *
from map_display import *
from interface import *
from game import *
from message_box import *
from find_path import *
from ammunition import *
from unit_base import *


class Play():
    debugging = False
    game_paused = False

    def __init__(self, master_screen, parent):
        # self.parent_clock = master_clock
        self.master_screen = master_screen

        self.screen = pygame.Surface(master_screen.get_size())
        self.screen.fill((255, 255, 255))
        self.screen.set_colorkey((255, 255, 255))
        self.screen_dim = master_screen.get_size()

        self.event_screen = []
        self.event_unit = []
        self.event_interface = []

        self.computer = player(self)
        self.human = player(self)
        # Initializing all modules

        self.map = Map()
        self.game_data = GameData(self)
        self.interface = Interface(self)
        self.message = Message(*master_screen.get_size())
        self.pathfinder = AStar(self)
        self.firearms = firearms(self)

        self.game_data.place_unit(command_center(self.computer, 20, 20, self))
        self.game_data.place_unit(command_center(self.human, 10, 10, self))

        m = resource_center(self.human, 14, 14)
        self.game_data.place_unit(m)
        self.human.units.append(m)

        m = helipad(self.human, 16, 16)
        self.human.units.append(m)
        self.game_data.place_unit(m)

        #  for debugging
        self.master_debug_list = []
        self.qwerty = pygame.image.load("units\\gray_out_area.bmp").convert_alpha()

        self.game_start = pygame.time.get_ticks()
        self.parent = parent
        # self.mainloop()

    def mainloop(self):
        Clock = pygame.time.Clock()
        while not self.game_paused:
            Clock.tick(50)

            self.interface.update()
            self.map.update()
            self.game_data.update()
            self.message.update()
            self.firearms.update()

            self.computer.update()
            self.human.update()

            self.screen.blit(self.map.screen, (0, 0))
            self.screen.blit(self.game_data.screen, (0, 0))
            self.screen.blit(self.interface.screen, (0, 0))
            self.screen.blit(self.message.screen, (0, 0))
            self.screen.blit(self.firearms.screen, (0, 0))

############################################################################
            if self.debugging:
                cx, cy = self.map.cur_pos
                wx, wy = self.map.window_w, self.map.window_h
                offx, offy = self.map.x_offset, self.map.y_offset
                for ix, iy in self.master_debug_list:
                    if cx < ix < cx+wx and cy < iy < cy+iy:
                        self.screen.blit(self.qwerty, ((ix-cx)*20+offx, (iy-cy)*20+offy))
############################################################################

            self.master_screen.blit(self.screen, (0, 0))
            pygame.display.update()

            if pygame.time.get_ticks() - self.game_start >= 1000:
                print pygame.time.get_ticks(), self.game_start
                self.game_paused = True
                self.parent.save_game()

    def debug(self, *args):
        x, y = args[0], args[1]
        self.master_debug_list.append((x, y))


class Menu():
    screen_dim = 800, 480

    def __init__(self):
        pygame.init()
        # self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode(self.screen_dim)   # , FULLSCREEN)

        self.play = Play(self.screen, self)

        self.menu_items = {"New game": self.play,
                           "Load game": 89375
                           }
        self.play.mainloop()

    def load_game(self):
        pass

    def save_game(self):
        import cPickle as pickle
        sys.setrecursionlimit(1000000)
        p = pickle.Pickler(open("temp.p","wb"))
        p.fast = True
        p.dump(self.play)

        pygame.quit()
        sys.exit()

    def credits(self):
        pass

import copy_reg


def surface_unpickler(surface_in_tuple):
    surf = pygame.image.fromstring(surface_in_tuple[0], surface_in_tuple[1], "RGBA")
    return surf


def surface_pickler(surface_to_pickle):
    string = pygame.image.tostring(surface_to_pickle, "RGBA")
    size = surface_to_pickle.get_size()
    return surface_unpickler, (string, size)


def pixelarray_unpickler(surface_in_tuple):
    surf = pygame.image.fromstring(surface_in_tuple[0], surface_in_tuple[1], "RGBA")
    pixel_array = pygame.PixelArray(surf)
    return pixel_array


def pixelarray_pickler(pixelarray_to_pickle):
    surface_to_pickle = pixelarray_to_pickle.make_surface()
    string = pygame.image.tostring(surface_to_pickle, "RGBA")
    size = surface_to_pickle.get_size()
    return pixelarray_unpickler, (string, size)


def clock_unpickler(clock_in_data):
    return pygame.time.Clock()


def clock_pickler(clock):
    return clock_unpickler, lambda: "String_Clock"

copy_reg.pickle(pygame.Surface, surface_pickler, surface_unpickler)
copy_reg.pickle(pygame.PixelArray, pixelarray_pickler, pixelarray_unpickler)
copy_reg.pickle(pygame.time.Clock, clock_pickler, clock_unpickler)




game = Menu()

