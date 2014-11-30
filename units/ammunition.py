__author__ = 'Edwin Clement'
import pygame
import math


class ammunition:
    speed = 0
    point_to_decrease = 0
    distance_traveled = 0

    def __init__(self, (x, y), angle, ammunition_type):
        self.start_position = (x, y+1)
        self.angle = angle
        self.type = ammunition_type
        self.time_fired = pygame.time.get_ticks()


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

    def add(self, firearm):
        if isinstance(firearm, ammunition):
            self.ammunition_list.append(firearm)
            firearm.image = pygame.transform.rotate(self.bullet_images[firearm.type], math.degrees(firearm.angle)) #  firearm.angle)
            # firearm.image = self.bullet_images[firearm.type]
            return True
        else:
            return None

    def remove_out_of_range(self):
        cr = 0
        al = self.ammunition_list
        while cr < len(self.ammunition_list):
            al[cr].distance_traveled = (pygame.time.get_ticks() - al[cr].time_fired) * self.get_speed[al[cr].type]
            if al[cr].distance_traveled > self.get_range[al[cr].type]:
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

        self.dirty_rect = []

        for t in self.ammunition_list:
            x, y = t.start_position
            u_dx, u_dy = t.distance_traveled * math.cos(t.angle), t.distance_traveled * -math.sin(t.angle)
            dx, dy = math.floor(u_dx), math.floor(u_dy)

            fx, fy = x + dx, y + dy
            # print fx, fy
            if self.x0 < fx < self.x1 and self.y0 < fy < self.y1:

                rel_x = fx - self.x0
                rel_y = fy - self.y0

                blit_x = rel_x*20 + (u_dx - dx)*20
                blit_y = rel_y*20 + (u_dy - dy)*20
                self.dirty_rect.append(pygame.Rect(blit_x-10, blit_y-10, 30, 30))
                self.screen.blit(t.image, (blit_x, blit_y))
