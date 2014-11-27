__author__ = 'Edwin Clement'
import pygame
from pygame.locals import *

pygame.init()
screen = pygame.display.set_mode((800, 600))


class unit_non_attacking:
    type = "building"
    destroyed = False
    frame_delay_time = 150
    cost = 0

    def __init__(self, allegiance, x, y):
        # data about itself
        self.allegiance = allegiance
        self.position = [x, y]
        self.image_file = "units/" + self.image_file

        # image data
        i = pygame.image.load(self.image_file).convert()
        im = pygame.Surface(i.get_size())
        im.set_colorkey((0, 128, 128))
        im.blit(i, (0, 0))

        px_image = pygame.PixelArray(im)

        self.image_idle = []
        self.no_of_frames = len(px_image)/(self.w*20)
        for t in range(self.no_of_frames):
            self.image_idle.append(px_image[t*(self.w*20):t*(self.w*20)+(self.h*20)-1, 0:(self.h*20)-1].make_surface())
        self.image_destroyed = px_image[0:self.w*20, self.h*20:(self.h*20)*2-1].make_surface()

        self.selection_image = pygame.transform.scale(px_image[0:self.w*20, 0:(self.h*20)-1].make_surface(), (40, 40))

        # used for blitting
        self.display_image = pygame.Surface((self.w*20-1, self.h*20-1))

        # Essential data on itself
        self.time_last_updated = pygame.time.get_ticks()-1000
        self.frame_no = -1

        # other data relevant to stuff
        self.health = self.total_health

        self.idle = True
        self.task_done = 100
        self.time_task_started = None
        self.total_time_for_task = 0
        self.task_args = []
        self.task_doing_name = ""
        self.task_list = {}

        # for CC to place units
        self.wait = False

    def increase_frame_no(self):
        if self.frame_no >= (self.no_of_frames-1):
            self.frame_no = 0
            return self.frame_no
        else:
            self.frame_no += 1
            return self.frame_no

    def update(self):
        self.any_other_stuff()
        if self.destroyed:
            self.display_image.blit(self.image_destroyed, (0, 0))
        else:
            if pygame.time.get_ticks() - self.time_last_updated >= self.frame_delay_time:
                self.increase_frame_no()
                self.display_image.blit(self.image_idle[self.frame_no], (0, 0))
                self.time_last_updated = pygame.time.get_ticks()

        if not self.idle and not self.wait:
            curtime = pygame.time.get_ticks()
            time_done = curtime - self.time_task_started
            self.task_done = time_done * 100 / self.total_time_for_task

            if self.task_done >= 100:
                self.do_task()

                self.idle = True
                self.task_done = 100
                self.time_task_started = None
                self.total_time_for_task = 0
                self.task_args = []
                self.task_doing_name = ""

    def got_hit(self, points):
        if self.health - points >= 0:
            self.health = self.health - points
        else:
            self.destroyed = True
            self.health = 0

    def get_free_neighbour(self):
        x, y, w, h = self.position[0], self.position[1], self.w, self.h

        directions = [(-1, -1), (0, -1), (1, -1), (-1, 0), (1, 0), (-1, 1), (0, 1), (1, 1)]
        occupied = set([])
        for my in range(y, y+h):
            for mx in range(x, x+w):
                occupied.add((mx, my))

        all_cover = set([])
        for s in occupied:
            for q in directions:
                all_cover.add((s[0]+q[0], s[1]+q[1]))
        actual_neighbours = all_cover - occupied
        actual_neighbours_free = []
        smap = self.allegiance.parent.game_data.places_truly_empty

        for (tx, ty) in actual_neighbours:
            if smap[ty][tx] == 1:
                actual_neighbours_free.append((tx,  ty))

        return actual_neighbours_free

    def do_selection(self, sel):
        pass

    def do_task(self):
        pass

    def any_other_stuff(self):
        pass

    def right_click_handle(self):
        pass


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

    idle = True  # just for maintaining conformity

    cur_direction = (0, -1)
    moving = False
    move_path = []
    move_progress = 0  # in percent
    time_since_last_inc = 0
    speed = 200  # (ms) will be override
    dx, dy = 0, 0
    # time interval between moves

    selection_options = {
    }

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
                if self.move_progress >= self.speed:
                    self.allegiance.parent.game_data.move_unit(self, self.position, self.cur_direction)
                    # self.position[0] += self.cur_direction[0]
                    # self.position[1] += self.cur_direction[1]
                    self.position = self.position[0] + self.cur_direction[0], self.position[1] + self.cur_direction[1]
                    self.move_progress = 0
                    self.dx, self.dy = 0, 0
                    self.cur_direction = self.move_path.pop(0)
                    self.time_since_last_inc = pygame.time.get_ticks()
                else:
                    if pygame.time.get_ticks() - self.time_since_last_inc >= self.speed:
                        move_per_20 = (self.move_progress/self.speed)*20.0
                        self.dx, self.dy = self.cur_direction[0]*move_per_20, self.cur_direction[1]*move_per_20

                        if self.cur_direction[0] == 0:
                            self.dx = 0
                        if self.cur_direction[1] == 0:
                            self.dy = 0
                        self.move_progress += 1.0
                        self.time_since_last_inc = pygame.time.get_ticks()
            else:
                self.moving = False
                self.move_path = []
                self.move_progress = 0  # in percent
                self.time_since_last_inc = pygame.time.get_ticks()

    def move(self, tx, ty):
        self.move_path = self.allegiance.parent.pathfinder.get_path((self.position[0], self.position[1]), (tx, ty))
        print self.move_path
        if self.move_path:
            self.moving = True
            self.move_progress = 0  # in percent
            self.cur_direction = self.move_path.pop(0)

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

    def do_selection(self, sel):
        pass

    def right_click_handle(self, x, y):
        #print x, y, 'gsege'
        if self.allegiance.parent.game_data.places_truly_empty[y][x]:
            print "Moving"
            self.move(x, y)
        else:
            click = self.allegiance.parent.game_data.get_unit(x, y)
            print click
            print click[0].allegiance
        pass


class Hovercraft(unit_attacking):
    name = "Hovercraft"
    cost = 400
    total_health = 500

    range = 5
    time_for_reload = 700
    speed = 10

    image_file = "Hovercraft.bmp"

    w, h = 1, 1


class Copter(unit_attacking):
    name = "Copter"
    cost = 700
    total_health = 200

    range = 10
    time_for_reload = 700
    speed = 14

    image_file = "Copter.bmp"

    w, h = 1, 1


class Paladin(unit_attacking):
    name = "Paladin"
    cost = 400
    total_health = 500

    range = 10
    time_for_reload = 1000
    speed = 4

    image_file = "Paladin.bmp"

    w, h = 1, 1


class Mobile_Missile(unit_attacking):
    name = "Mobile Missile"
    cost = 400
    total_health = 500

    range = 5
    time_for_reload = 1000
    speed = 1

    image_file = "Mobile_Missile.bmp"

    w, h = 1, 1


class Gattling_Gun(unit_attacking):
    name = "Gattling Gun"
    cost = 400
    total_health = 500

    range = 8
    time_for_reload = 1000
    speed = 1

    image_file = "Gattling_Gun.bmp"

    w, h = 1, 1
########################################################################################################################


class resource_center(unit_non_attacking):
    name = "Resource Center"
    total_health = 750
    cost = 100
    power = 2

    image_file = "resource_center.bmp"
    w, h = 2, 3

    time_last_mined = 0
    time_for_one_operation = 3000
    amount_per_operation = 200

    def __init__(self, allegiance, x, y):
        unit_non_attacking.__init__(self, allegiance, x, y)
        self.time_last_mined = pygame.time.get_ticks()

    def any_other_stuff(self):
        if pygame.time.get_ticks() - self.time_last_mined >= self.time_for_one_operation:
            self.allegiance.money += self.amount_per_operation
            self.time_last_mined = pygame.time.get_ticks()

    selection_options = {
    }


class artillery_shop(unit_non_attacking):
    name = "Artillery Shop"
    total_health = 300
    cost = 300
    power = 3

    image_file = "artillery_shop.bmp"
    w, h = 2, 3

    # implement low power shutdown # for checking ## self.allegiance.low_power

    selection_options = {
    }


class helipad(unit_non_attacking):
    name = "Helipad"
    total_health = 300
    cost = 500
    power = 5

    # implement low power shutdown # for checking ## self.allegiance.low_power

    image_file = "helipad.bmp"
    w, h = 2, 3

    selection_options = {'Copter': Copter("", -1, -1).selection_image}

    def __init__(self, allegiance, x, y):
        unit_non_attacking.__init__(self, allegiance, x, y)
        self.task_list = {
            'Copter': (Copter, 1000),
        }

    def do_task(self):
        free_neighbour = self.get_free_neighbour()[0]
        if free_neighbour:
            u = self.task_list[self.task_doing_name][0](self.allegiance, free_neighbour[0], free_neighbour[1])

            self.allegiance.units.append(u)
            self.allegiance.parent.game_data.place_unit(u)
        else:
            self.allegiance.parent.message.put_message("No free Area around the Helipad")

    def do_selection(self, sel_option):
        if self.idle:
            if self.allegiance.money - self.task_list[sel_option][0].cost >= 0:
                self.allegiance.money -= self.task_list[sel_option][0].cost
                self.idle = False
                self.wait = False
                self.task_doing_name = sel_option
                self.time_task_started = pygame.time.get_ticks()
                self.task_done = 0
                if not self.allegiance.low_power:
                    self.total_time_for_task = self.task_list[sel_option][1]
                else:
                    self.total_time_for_task = self.task_list[sel_option][1]*1.1
                self.task_args = [self.allegiance]
            else:
                self.allegiance.parent.message.put_message("Not enough money")


class generator(unit_non_attacking):
    name = "Generator"
    total_health = 300
    cost = 200

    power = 0

    image_file = "generator.bmp"
    w, h = 2, 3

    selection_options = {
    }


class command_center(unit_non_attacking):
    name = "Command Center"
    total_health = 1000
    cost = 1000
    power = 0

    image_file = "command_center.bmp"
    w, h = 3, 3

    selection_options = {
        'Resource Center': resource_center("", -1, -1).selection_image,
        'Artillery Shop': artillery_shop("", -1, -1).selection_image,
        'Helipad': helipad("", -1, -1).selection_image,
        'Generator': generator("", -1, -1).selection_image
    }

    def __init__(self, allegiance, x, y, parent):
        unit_non_attacking.__init__(self, allegiance, x, y)
        self.parent = parent
        self.positioning = False
        self.place_pos = None, None

        self.task_list = {
            'Resource Center': (resource_center, 6000),
            'Artillery Shop': (artillery_shop, 7000),
            'Helipad': (helipad, 10000),
            'Generator': (generator, 3000),
            'positioning': (None, 60000)
        }

    def do_task(self):
        if self.parent.game_data.is_place_truly_empty(*self.task_args[1:3]):
            u = self.task_list[self.task_doing_name][0](*self.task_args)
            self.allegiance.units.append(u)
            self.parent.game_data.place_unit(u)

    def do_selection(self, sel_option):
        if self.idle:
            if self.allegiance.money - self.task_list[sel_option][0].cost >= 0:
                self.allegiance.money = self.allegiance.money - self.task_list[sel_option][0].cost
                self.idle = False
                self.wait = True
                self.task_doing_name = sel_option
                self.time_task_started = None
                self.task_done = 0
                self.total_time_for_task = self.task_list[sel_option][1]
                self.task_args = [self.allegiance]
                self.positioning = True

    def positioning_completed(self):
        self.wait = False
        self.positioning = False
        self.time_task_started = pygame.time.get_ticks()
        self.task_args = self.task_args + list(self.place_pos)
        pass

    def any_other_stuff(self):
        pass