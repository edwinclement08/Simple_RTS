__author__ = 'Edwin Clement'
import json
import pygame
import sys
from pygame.locals import *
sys.path[0:0] = ("units",)
import unit_base


class player():
    def __init__(self, parent):
        self.parent = parent
        self.money = 5000
        self.power = 1
        self.units = []

        self.low_power = False
        self.req_power = 1.0

    def update(self):
        self.power_update()
        self.check_for_enough_power()

        g = 0
        while g < len(self.units):
            if self.units[g].destroyed and (pygame.time.get_ticks() - self.units[g].time_since_destroyed) > 3000:
                a = self.units.pop(g)
                self.parent.game_data.delete_unit(a)
                del a
            g += 1

    def power_update(self):
        p = 1
        for t in self.units:
            if isinstance(t, unit_base.generator):
                if not t.destroyed:
                    p += 5  # power supplied by one generator
        self.power = p

    def check_for_enough_power(self):
        req_power = 0
        for t in self.units:
            if isinstance(t, unit_base.resource_center) or isinstance(t, unit_base.artillery_shop) or \
                    isinstance(t, unit_base.helipad):
                if not t.destroyed:
                    req_power += t.power
        self.req_power = req_power
        if self.power < self.req_power:
            self.low_power = True
        else:
            self.low_power = False


class GameData:
    def __init__(self, parent):
        self.time = 0
        self.units = []
        self.places_occupied = [[0]*100 for d in range(100)]
        self.places_truly_empty = [[0]*100 for d in range(100)]
        self.marked_place = set()
        self.parent = parent

        self.screen = pygame.Surface((self.parent.map.window_w*20, self.parent.map.window_h*20)).convert()
        self.screen.set_colorkey((0, 128, 128))

        self.conv = lambda x, y: ((x-self.parent.map.x_offset)/20+self.parent.map.cur_pos[0],
                                 (y-self.parent.map.y_offset)/20+self.parent.map.cur_pos[1])

        self.selection = None

    def update(self):
        self.screen.fill((0, 128, 128))

        for m in self.units:
            if issubclass(m[0].__class__, unit_base.unit_attacking):
                x = (m[0].position[0] - self.parent.map.cur_pos[0])*20+self.parent.map.x_offset + m[0].dx
                y = (m[0].position[1] - self.parent.map.cur_pos[1])*20+self.parent.map.y_offset + m[0].dy
            else:
                x = (m[0].position[0] - self.parent.map.cur_pos[0])*20+self.parent.map.x_offset
                y = (m[0].position[1] - self.parent.map.cur_pos[1])*20+self.parent.map.y_offset
            m[0].update()
            self.screen.blit(m[0].display_image, (x, y))

        for y in xrange(100):
            for x in xrange(100):
                self.places_truly_empty[y][x] = self.is_place_truly_empty(x, y)

    def place_unit(self, unit):
        x, y = unit.position
        if 0 < x < 99 and 0 < y < 99:
            if self.parent.map.is_cell_free(x, y) and self.is_place_empty(x, y):
                self.units.append([unit, x, y])
                unit.position = x, y
                sw, sh = unit.w, unit.h
                for my in xrange(sh):
                    for mx in xrange(sw):
                        self.places_occupied[y+my][x+mx] = 1

    def move_unit(self, unit, (x, y), direction):
        w, h = unit.w, unit.h
        dx, dy = x + direction[0], y + direction[1]

        for ly in xrange(y, y+h):
            for lx in xrange(x, x+w):
                self.places_occupied[ly][lx] = 0

        for ly in xrange(dy, dy+h):
            for lx in xrange(dx, dx+w):
                self.places_occupied[ly][lx] = 1

    def set_as_marked(self, (x, y)):
        if self.is_place_truly_empty(x, y):
            self.marked_place.add((x, y))

    def remove_mark(self, (x, y)):
        if (x, y) in self.marked_place:
            self.marked_place.remove((x, y))

    def is_place_empty(self, x, y):
        if not self.places_occupied[y][x] and not((x, y) in self.marked_place):
            return True
        else:
            return False

    def is_place_truly_empty(self, x, y):
        if not self.places_occupied[y][x] and self.parent.map.is_cell_movable(x, y)\
                and not((x, y) in self.marked_place):
            return 1
        else:
            return 0

    def get_unit(self, x, y):
        # print x, y,
        if not self.is_place_empty(x, y):
            # print "gotcha"
            for w in self.units:
                x0, y0 = w[0].position[0], w[0].position[1]
                sw, sh = w[0].w, w[0].h
                for my in xrange(y0, y0+sh):
                    for mx in xrange(x0, x0+sw):
                        if (mx, my) == (x, y):
                            return w[0], x0, y0, sw, sh
        else:
            # print "man"
            pass
        return None

    def select_unit(self, x, y, allegiance):
        if not self.is_place_empty(x, y):
            for w in self.units:
                x0, y0 = w[0].position[0], w[0].position[1]
                sw, sh = w[0].w, w[0].h
                for my in xrange(y0, y0+sh):
                    for mx in xrange(x0, x0+sw):
                        if (mx, my) == (x, y):
                            if allegiance == w[0].allegiance:
                                self.selection = [w[0], x0, y0, sw, sh]
                                return w[0], x0, y0, sw, sh
        return None

    def select_units(self, m0, n0, m1, n1, allegiance):
        anything_present = False
        points_of_interest = []
        selection = set([])
        x0, y0 = self.conv(m0, n0)
        x1, y1 = self.conv(m1, n1)
        for x in xrange(x0, x1+1):
            for y in xrange(y0, y1+1):
                if not self.is_place_empty(x, y):
                    anything_present = True
                    points_of_interest.append((x, y))
        if anything_present:
            print self.units
            for x, y in points_of_interest:
                for w in self.units:
                    if (w[0].position[0], w[0].position[1]) == (x, y):
                        x0, y0 = w[0].position[0], w[0].position[1]
                        # x1, y1 = w[0].w + w[0].x, w[0].h + w[0].y
                        if allegiance == w[0].allegiance:
                            selection.add((w[0], x0, y0, w[0].w, w[0].h))
            self.selection = list(selection)
            return list(selection)
        return None

    def delete_unit(self, unit):
        print unit, self.units
        self.units.remove([unit, unit.position[0], unit.position[1]])
        sw, sh = unit.w, unit.h
        x, y = unit.position[0], unit.position[1]
        for my in xrange(sh):
            for mx in xrange(sw):
                self.places_occupied[y+my][x+mx] = 0