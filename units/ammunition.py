__author__ = 'Edwin Clement'
import pygame
import math


class ammunition:
    speed = 0
    point_to_decrease = {'bullet': 10,
                         'ecm': 20,
                         'missile': 13,
                         'flame thrower': 40}
    distance_traveled = 0

    def __init__(self, (x, y), angle, ammunition_type, parent_unit):
        self.start_position = (x, y)
        self.angle = angle
        self.type = ammunition_type
        self.time_fired = pygame.time.get_ticks()
        self.red_points = self.point_to_decrease[ammunition_type]
        self.has_hit = False
        self.parent = parent_unit


class firearms:
    image_file = "units\\ammunition.bmp"
    get_speed = {'bullet': 0.005,
                 'ecm': 0.008,
                 'missile': 0.004,
                 'flame thrower': 0.002}
    get_range = {'bullet': 10,
                 'ecm': 10,
                 'missile': 20,
                 'flame thrower': 5}

    def __init__(self, parent):
        self.parent = parent
        p_map = self.parent.map
        self.screen_width = p_map.window_w*20
        self.screen_height = p_map.window_h*20
        self.x_offset = p_map.x_offset
        self.y_offset = p_map.y_offset
        self.x0, self.y0, self.x1, self.y1 = 0, 0, 0, 0

        self.screen = pygame.Surface((self.screen_width*20, self.screen_height*20))

        self.dirty_rect = []

        self.screen.fill((0, 0, 0))
        self.screen.set_colorkey((0, 0, 0))

        self.ammunition_list = []

        w_image = pygame.image.load(self.image_file)
        px_array = pygame.PixelArray(w_image)

        self.bullet_images = {}
        num_bullet = ['flame thrower', 'ecm', 'bullet', 'missile']

        for i, name in enumerate(num_bullet):
            self.bullet_images[name] = px_array[i*10:i*10+10, 0:10].make_surface().convert()
            self.bullet_images[name].set_colorkey((0, 128, 128))

    def add(self, firearm_name, (self_x, self_y), (enemy_x, enemy_y), parent_unit):
        angle = math.atan2(enemy_x-self_x, enemy_y-self_y)
        angle += math.pi/2
        # angle = math.pi/2.0

        self.parent.debug(self_x, self_y)

        if firearm_name in self.get_range:
            ammo = ammunition((self_x, self_y), angle, firearm_name, parent_unit)
            self.ammunition_list.append(ammo)

            ammo.image = pygame.transform.rotate(self.bullet_images[ammo.type], math.degrees(ammo.angle + math.pi))

            return True
        else:
            return None

    def remove_out_of_range(self):
        cr = 0
        al = self.ammunition_list
        while cr < len(self.ammunition_list):
            al[cr].distance_traveled = (pygame.time.get_ticks() - al[cr].time_fired) * self.get_speed[al[cr].type]
            if al[cr].distance_traveled > self.get_range[al[cr].type] or al[cr].has_hit:
                al.remove(al[cr])
                cr -= 1
            cr += 1

    def update(self):
        if self.dirty_rect:
            for rt in self.dirty_rect:
                pygame.draw.rect(self.screen, (0, 0, 0), rt, 0)

        self.remove_out_of_range()

        cp_x, cp_y = self.parent.map.cur_pos
        self.x0, self.y0, self.x1, self.y1 = cp_x, cp_y, cp_x + self.screen_width, cp_y + self.screen_height

        offset_x, offset_y = self.parent.map.x_offset, self.parent.map.y_offset

        self.dirty_rect = []

        for t in self.ammunition_list:
            x, y = t.start_position
            u_dx, u_dy = t.distance_traveled * -math.cos(t.angle), t.distance_traveled * math.sin(t.angle)
            dx, dy = math.floor(u_dx), math.floor(u_dy)

            cdx, cdy = int(x + math.ceil(u_dx)), int(y + math.ceil(u_dy))
            fx, fy = int(x + dx), int(y + dy)

            if self.x0 < (fx-cp_x)*20+offset_x < self.x1 and self.y0 < (fy-cp_y)*20+offset_y< self.y1 or \
                    self.x0 < (cdx-cp_x)*20+offset_x < self.x1 and self.y0 < (cdy-cp_y)*20+offset_y< self.y1:
                rel_x = fx - self.x0
                rel_y = fy - self.y0

                blit_x = rel_x*20 + (u_dx - dx)*20 + offset_x
                blit_y = rel_y*20 + (u_dy - dy)*20 + offset_y
                self.dirty_rect.append(pygame.Rect(blit_x-10, blit_y-10, 30, 30))
                self.screen.blit(t.image, (blit_x, blit_y))

            if self.parent.game_data.has_any_unit(fx, fy):
                unit_data = self.parent.game_data.get_unit(fx, fy)[0]
                if unit_data != t.parent:
                    unit_data.got_hit(t.red_points)
                    t.has_hit = True
            elif self.parent.game_data.has_any_unit(cdx, cdy):
                unit_data = self.parent.game_data.get_unit(cdx, cdy)[0]
                if unit_data != t.parent:
                    unit_data.got_hit(t.red_points)
                    t.has_hit = True
            elif not self.parent.map.is_cell_free(fx, fy):
                t.has_hit = True
