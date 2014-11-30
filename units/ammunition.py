__author__ = 'Edwin Clement'
import pygame


class ammunition:
    speed = 0
    point_to_decrease = 0
    distance_traveled = 0

    def __init__(self, (x, y), angle, ammunition_type):
        self.start_position = (x, y)
        self.angle = angle
        self.type = ammunition_type
        self.time_fired = pygame.time.get_ticks()


class firearms:
    image_file = "ammunition.bmp"
    get_speed = {'bullet': 100,
                 'ecm': 500,
                 'missile': 300,
                 'flame thrower': 200}
    get_range = {'bullet': 100,
                 'ecm': 500,
                 'missile': 300,
                 'flame thrower': 200}

    def __init__(self, parent):
        self.parent = parent
        p_map = self.parent.map
        self.screen_width = p_map.window_w*20
        self.screen_height = p_map.window_h*20
        self.x_offset = p_map.x_offset
        self.y_offset = p_map.y_offset
        self.x0, self.y0, self.x1, self.y1 = p_map.x0, p_map.y0, p_map.x1, p_map.y1

        self.screen = pygame.Surface((self.screen_width*20, self.screen_height*20))
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
            return True
        else:
            return None

    def remove_out_of_range(self):
        cr = 0
        al = self.ammunition_list
        while cr < len(self.ammunition_list):
            al[cr].distance_traveled = al[cr].time_fired * self.get_speed[al[cr].type]
            if al[cr].distance_traveled > self.get_range[al[cr].type]:
                al.remove(al[cr])
                cr -= 1
            cr += 1

    # def






