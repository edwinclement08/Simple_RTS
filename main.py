__author__ = 'Edwin Clement'
import pygame
import sys
from pygame.locals import *
from map_display import *
from interface import *
from game import *
from find_path import *
sys.path[0:0] = ("units",)
from unit_base import *
from message_box import *
from find_path import *


class Main():
    screen_dim = w, h = 800, 480

    def __init__(self):
        pygame.init()

        self.event_screen = []
        self.event_unit = []
        self.event_interface = []

        self.screen = pygame.Surface(self.screen_dim)
        self.screen.fill((255, 255, 255))
        self.screen.set_colorkey((255, 255, 255))

        self.true_screen = pygame.display.set_mode(self.screen_dim)     # , FULLSCREEN)

        self.computer = player(self)
        self.human = player(self)
        # Initializing all modules
        self.map = Map()
        self.game_data = GameData(self)
        self.interface = Interface(self)
        self.message = Message(self.w, self.h)
        self.pathfinder = AStar(self)

        self.game_data.place_unit(command_center(self.human, 10, 10, self))

        m = resource_center(self.human, 14, 14)
        self.game_data.place_unit(m)
        self.human.units.append(m)
        m = helipad(self.human, 16, 16)
        self.human.units.append(m)
        self.game_data.place_unit(m)

        self.first_run = 1

        self.mainloop()

    def mainloop(self):
        clock = pygame.time.Clock()
        running = 1
        while running:
            clock.tick(40)
            # print clock.get_fps()
            self.interface.update()
            self.map.update()
            self.game_data.update()
            self.message.update()

            self.computer.update()
            self.human.update()

            self.screen.blit(self.map.screen, (0, 0))
            self.screen.blit(self.game_data.screen, (0, 0))
            self.screen.blit(self.interface.screen, (0, 0))
            self.screen.blit(self.message.screen, (0, 0))

            self.true_screen.blit(self.screen, (0, 0))
            pygame.display.update()

runtime = Main()
