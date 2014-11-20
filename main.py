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

        self.true_screen = pygame.display.set_mode(self.screen_dim)  #,FULLSCREEN)

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

            if self.first_run:
                self.first_run += 1
            if self.first_run == 290:

                startx, starty, endx, endy = (0, 10, 12, 0)
                c = self.pathfinder.get_path((0, 10), (12, 0))
                print "dsfv", c
                for t in c:
                    startx += t[0]
                    starty += t[1]

                print "yo Man (", startx, ",", starty, ") and ", endx, endy
            if self.first_run == 467:
                self.first_run = False
                startx, starty, endx, endy = (0, 10, 12, 0)
                c = self.pathfinder.get_path((0, 10), (12, 0))
                print "dsfv", c
                for t in c:
                    startx += t[0]
                    starty += t[1]

                print "yo Man (", startx, ",", starty, ") and ",endx,endy

            self.true_screen.blit(self.screen, (0, 0))
            pygame.display.update()

runtime = Main()



# ##############################################################
# ####### Implement return 1 to prevent problems (running) #####
# ##############################################################
#     def check_events(self):
#         for event in pygame.event.get():
#             if event.type == QUIT:
#                sys.exit()
#             elif event.type == KEYDOWN:
#                 q = {
#                     K_a: ('screen', "left"),
#                     K_w: ('screen', "up"),
#                     K_s: ('screen', "down"),
#                     K_d: ('screen', "right"),
#                     K_LEFT: ('screen', "left"),
#                     K_UP: ('screen', "up"),
#                     K_DOWN: ('screen', "down"),
#                     K_RIGHT: ('screen', "right"),
#
#                     K_DELETE: ('unit','delete'),
#                     K_SPACE: ('unit','select'),
#
#                     K_ESCAPE: ('interface', "escape"),
#                     K_RETURN: ('interface', "return")
#                 }
#                 try:
#                     if q[event.key][0] == 'screen':
#                         self.event_screen.append(q[event.key])
#                     elif q[event.key][0] == 'unit':
#                         self.event_unit.append(q[event.key])
#                     elif q[event.key][0] == 'interface':
#                         self.event_interface.append(q[event.key])
#                 except KeyError:
#                     pass
#  2.
#  3.
#  4.
#  5.
#  6. pygame.display.set_caption('Hello World!')
#  7. while True: # main game loop
#  8.     for event in pygame.event.get():
#  9.         if event.type == QUIT:
# 10.             pygame.quit()
# 11.             sys.exit()
# 12.     pygame.display.update()