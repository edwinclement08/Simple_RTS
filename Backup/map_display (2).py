__author__ = 'Edwin Clement'
import json
import pygame
import sys
from pygame.locals import *

class Map:
    image_file = 'terrain.bmp'
    data_file = 'map.json'
    cur_pos = 55,62
    window_w,window_h =30,23        # No. of tiles
    x_offset, y_offset = 20,45


    def __init__(self):
        pygame.init()
        self.screen = pygame.Surface((self.window_w*20,self.window_h*20)).convert()
        self.screen.fill((255,255,255))
        self.screen.set_colorkey((255,255,255))

        self.map = json.load(open(self.data_file))
        ml = self.map["main_layer"]
        ol = self.map["overlay"]
        self.main_layer = [ml[a:a+100] for a in range(0,len(ml),100)]
        self.overlay = [ol[a:a+100] for a in range(0,len(ol),100)]

        self.image = pygame.image.load(self.image_file).convert()
        self.main_pixel_array = mpa = pygame.PixelArray(self.image)

        pic_data = self.map['tile_data']
        self.image_dict={}
        for m in pic_data:
            x,y = m[2]
            x,y = x*20,y*20

            sub_image = mpa[x:x+20,y:y+20]
            code = m[0]
            self.image_dict[code] = sub_image.make_surface(),str(m[1])
            self.image_dict[code][0].set_colorkey((255,255,255), pygame.RLEACCEL)

        pp = pygame.Surface((20,20)).convert()
        pp.set_colorkey((255,255,255))
        pp.fill((255,255,255))
        self.image_dict[0] = pp,"nothing.transparent"

        ######### Optimize above later

        self.update()

    def set_cur_pos(self, x=0, y=0):
        if not(x < 0 or y < 0 or x+self.window_w >= 100 or y+self.window_h >= 100):
            print x,y
            self.cur_pos = x,y
        self.update()

    def update(self):
        y0 = 0
        for y in range(self.cur_pos[1],self.cur_pos[1]+self.window_h):
            x0 = 0
            for x in range(self.cur_pos[0],self.cur_pos[0]+self.window_w):
                self.screen.blit(self.image_dict[self.main_layer[y][x]][0],(x0*20+self.x_offset,y0*20+self.y_offset))
                x0 += 1
            y0+=1

        y0 = 0
        for y in range(self.cur_pos[1],self.cur_pos[1]+self.window_h):
            x0 = 0
            for x in range(self.cur_pos[0],self.cur_pos[0]+self.window_w):
                self.screen.blit(self.image_dict[self.overlay[y][x]][0],(x0*20+self.x_offset,y0*20+self.y_offset))
                x0 += 1
            y0+=1

    def is_cell_free(self,x,y):
        if self.image_dict[self.main_layer[y][x]][1] in ["grass.rough","grass.smooth"]:
            return True
        else:
            return False

    def get_terrain_type(self,x,y):
        if self.image_dict[self.overlay[y][x]][1] == "nothing.transparent":
            return self.image_dict[self.main_layer[y][x]][1].split('.')
        else:
            return self.image_dict[self.overlay[y][x]][1].split('.')

#####################################################################################
####################### For DEBUGGING Purposes ######################################
#
# pygame.init()
# scream = pygame.display.set_mode((800,600))
#
# s = Map()
# s.update()
# scream.blit(s.screen,(0,0))
# pygame.display.update()
# r = pygame.time.Clock()
# print s.get_terrain_type(11,63)
# while 1:
#     for event in pygame.event.get():
#         if event.type == QUIT:
#             pygame.quit()
#             sys.exit()
#         elif event.type == KEYDOWN:
#             q = {
#                 K_a: ('screen', "left"),
#                 K_w: ('screen', "up"),
#                 K_s: ('screen', "down"),
#                 K_d: ('screen', "right"),
#                 K_LEFT: ('screen', "left"),
#                 K_UP: ('screen', "up"),
#                 K_DOWN: ('screen', "down"),
#                 K_RIGHT: ('screen', "right"),
#
#                 K_DELETE: ('unit','delete'),
#                 K_SPACE: ('unit','select'),
#
#                 K_ESCAPE: ('interface', "escape"),
#                 K_RETURN: ('interface', "return")
#             }
#             try:
#                 if q[event.key][1] == 'left':
#                     s.set_cur_pos(s.cur_pos[0]-1,s.cur_pos[1])
#                 if q[event.key][1] == 'right':
#                     s.set_cur_pos(s.cur_pos[0]+1,s.cur_pos[1])
#                 if q[event.key][1] == 'up':
#                     s.set_cur_pos(s.cur_pos[0],s.cur_pos[1]-1)
#                 if q[event.key][1] == 'down':
#                     s.set_cur_pos(s.cur_pos[0],s.cur_pos[1]+1)
#             except KeyError:
#                 pygame.quit()
#                 sys.exit()
#
#
#     s.update()
#     scream.blit(s.screen,(0,0))
#     pygame.display.update()
#
#
# pygame.quit()
####################################################################################