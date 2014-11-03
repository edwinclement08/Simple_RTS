__author__ = 'Edwin Clement'
import pygame, sys
from pygame.locals import *
from map_display import *
from interface import *

class Main():
    screen_dim = w,h = 800, 480

    def __init__(self):
        pygame.init()

        self.event_screen = []
        self.event_unit = []
        self.event_interface = []

        self.screen = pygame.Surface(self.screen_dim)
        self.screen.fill((255,255,255))
        self.screen.set_colorkey((255,255,255))

        self.true_screen = pygame.display.set_mode(self.screen_dim)
        self.map = Map()

        self.interface = Interface(self)


        self.mainloop()

    def mainloop(self):
        running = 1
        while running:
            self.check_events()
            self.screen.blit(self.map.screen,(0,0))
            self.screen.blit(self.interface.screen,(0,0))



            self.true_screen.blit(self.screen,(0,0))
            pygame.display.update()



##############################################################
####### Implement return 1 to prevent problems (running) #####
##############################################################
    def check_events(self):
        for event in pygame.event.get():
            if event.type == QUIT:
               sys.exit()
            elif event.type == KEYDOWN:
                q = {
                    K_a: ('screen', "left"),
                    K_w: ('screen', "up"),
                    K_s: ('screen', "down"),
                    K_d: ('screen', "right"),
                    K_LEFT: ('screen', "left"),
                    K_UP: ('screen', "up"),
                    K_DOWN: ('screen', "down"),
                    K_RIGHT: ('screen', "right"),

                    K_DELETE: ('unit','delete'),
                    K_SPACE: ('unit','select'),

                    K_ESCAPE: ('interface', "escape"),
                    K_RETURN: ('interface', "return")
                }
                try:
                    if q[event.key][0] == 'screen':
                        self.event_screen.append(q[event.key])
                    elif q[event.key][0] == 'unit':
                        self.event_unit.append(q[event.key])
                    elif q[event.key][0] == 'interface':
                        self.event_interface.append(q[event.key])
                except KeyError:
                    pass

runtime = Main()












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