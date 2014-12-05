__author__ = 'Edwin Clement'
import json
import pygame
import pygame.gfxdraw
if not pygame.font:
    print 'Warning, fonts disabled'
from pygame.locals import *
import sys
sys.path[0:0] = ("units",)
import unit_base
from message_box import *


class Interface:
    data_file = "Data\\interface.json"
    image_file = "Data\\interface.bmp"
    title_file = "Data\\title_bar.bmp"
    box_file = "Data\\box.bmp"
    mini_box_file = "Data\\mini_box.bmp"
    context_box_file = "Data\\context_box.bmp"
    mini_map_file = "Data\\mini_map.bmp"

    gold_file = "Data\\gold.bmp"
    power_file = "Data\\power.bmp"

    grey_area_file = "units\\gray_out_area.bmp"
    grey_file = "units\\gray_2_3.bmp"
    red_file = "units\\red_2_3.bmp"

    cursor_files = {"attack": "Data\\cursors\\attack.png",
                    "move": "Data\\cursors\\move1.png",
                    "select": "Data\\cursors\\select.png",
                    "default": "Data\\cursors\\cursor.png",
                    "normal": "Data\\cursors\\cursor.png",
                    }

    def __init__(self, parent):
        pygame.key.set_repeat(50, 100)
        self.parent = parent
        self.screen = pygame.Surface(parent.screen_dim).convert()
        self.screen.fill((255, 255, 255))
        self.screen.set_colorkey((255, 255, 255))

        self.title_bar = pygame.image.load(self.title_file).convert()
        self.box = pygame.image.load(self.box_file).convert()

        self.mini_map = pygame.image.load(self.mini_map_file).convert()
        self.mini_box = pygame.image.load(self.mini_box_file).convert()
        self.context_box = pygame.image.load(self.context_box_file).convert()

        self.gold_image = pygame.image.load(self.gold_file).convert()
        self.power_image = pygame.image.load(self.power_file).convert()
        self.power_image.set_colorkey((255, 255, 255))

        self.gray_area_image = pygame.image.load(self.grey_area_file).convert()
        self.grey_image = pygame.image.load(self.grey_file).convert()
        self.red_image = pygame.image.load(self.red_file).convert()

        pic_data = json.load(open(self.data_file))
        self.mother_of_images = pygame.image.load(self.image_file).convert()
        self.main_pixel_array = mpa = pygame.PixelArray(self.mother_of_images)
        self.image_dict = {}
        for m in pic_data:
            if m == "transparent_color":
                continue
            x1, y1, x2, y2 = pic_data[m]
            sub_image = mpa[x1:x2, y1:y2]
            self.image_dict[m] = sub_image.make_surface()

        # Mouse variables
        self.mouse_pos = pygame.mouse.get_pos()
        self.left_mouse_clicked = 0
        self.right_mouse_clicked = 0
        self.middle_mouse_clicked = 0
        self.time_last_moved = pygame.time.get_ticks()
        self.time_last_map_moved = pygame.time.get_ticks()
        self.dragging = 0
        self.drag_start = self.drag_st_x, self.drag_st_y = 0, 0
        self.drag_end = 0, 0

        self.c = [0, 0]

        self.font = pygame.font.Font(None, 26)
        self.small_font = pygame.font.Font(None, 16)
        self.medium_font = pygame.font.Font(None, 18)
        self.medium2_font = pygame.font.Font(None, 22)
        self.big_font = pygame.font.Font(None, 28)

        text = self.font.render("The Game v1.0", 1, (10, 10, 10))
        w, h = text.get_width(), text.get_height()
        self.title = text, w, h

        self.q = {
            K_a: (self.parent.map.move_pos, -1, 0),
            K_w: (self.parent.map.move_pos, 0, -1),
            K_s: (self.parent.map.move_pos, 0, +1),
            K_d: (self.parent.map.move_pos, +1, 0),
            K_LEFT: (self.parent.map.move_pos, -1, 0),
            K_UP: (self.parent.map.move_pos, 0, -1),
            K_DOWN: (self.parent.map.move_pos, 0, +1),
            K_RIGHT: (self.parent.map.move_pos, +1, 0),
            K_SPACE: (lambda rx, ry: None, 'stop', ""),

            K_DELETE: ((lambda rx, ry: None), 'delete', ''),
            K_ESCAPE: ((lambda rx, ry: None), "escape", ''),
            K_RETURN: ((lambda rx, ry: None), "return", '')
        }

        self.conv = self.xy_to_tile = lambda rx, ry: ((rx-self.parent.map.x_offset)/20+self.parent.map.cur_pos[0],
                                                     (ry-self.parent.map.y_offset)/20+self.parent.map.cur_pos[1])

        self.multiple_selected = False
        self.selected_unit = False
        self.image_for_selection = []
        self.selected_options = []
        self.selection_boxes_and_state = []
        self.multi_attacking_units = False

        self.multi_sel_image_init_points = []

        self.coord_of_the_sel_data_box = pygame.Rect(0, 0, 0, 0)

        # Cursor
        self.cursor_images = {}
        for w in self.cursor_files:
            self.cursor_images[w] = pygame.image.load(self.cursor_files[w]).convert_alpha()
        self.current_cursor = self.cursor_images["default"]
        pygame.mouse.set_visible(False)
        x, y = self.parent.map.x0, self.parent.map.y0
        w, h = self.parent.map.x1 - self.parent.map.x0, self.parent.map.y1 - self.parent.map.y0
        self.game_area = pygame.Rect(x, y, w, h)

        # placing
        self.placeable = False

        self.update()

    def update(self):
        # Mouse Cursor Setting
        x = (self.mouse_pos[0]-self.parent.map.x_offset)/20+self.parent.map.cur_pos[0]
        y = (self.mouse_pos[1]-self.parent.map.y_offset)/20+self.parent.map.cur_pos[1]

        ## handles Mouse cursor images
        if (not self.parent.game_data.is_place_empty(x, y)) and (self.selected_unit or self.multiple_selected) and \
                self.parent.game_data.get_unit(x, y) and \
                self.parent.game_data.get_unit(x, y)[0].allegiance == self.parent.computer:
            one_attacking_unit = self.selected_unit\
                and isinstance(self.selected_unit, unit_base.unit_attacking)
            self.multi_attacking_units = False
            if not self.multiple_selected:
                self.multi_attacking_units = False
            else:
                for k in self.multiple_selected:
                    if isinstance(k, unit_base.unit_attacking):
                        self.multi_attacking_units = True
                        break
                else:
                    self.multi_attacking_units = False
            if one_attacking_unit or self.multi_attacking_units:
                self.current_cursor = self.cursor_images["attack"]
        elif (self.selected_unit or self.multiple_selected) \
                and self.parent.map.is_cell_free(x, y) and self.parent.game_data.is_place_empty(x, y):
            if self.selected_unit and issubclass(self.selected_unit.__class__, unit_base.unit_attacking):
                self.current_cursor = self.cursor_images["move"]
            elif self.multiple_selected:
                for q in self.multiple_selected:
                    if issubclass(q.__class__, unit_base.unit_attacking):
                        self.current_cursor = self.cursor_images["move"]
            else:
                    self.current_cursor = self.cursor_images["normal"]
        elif self.parent.game_data.get_unit(x, y) and \
                self.parent.game_data.get_unit(x, y)[0].allegiance == self.parent.human:
            self.current_cursor = self.cursor_images["select"]
        else:
            self.current_cursor = self.cursor_images["normal"]

        # the borders
        # qqq = pygame.time.get_ticks()
        self.screen.fill((255, 255, 255))

        self.screen.blit(self.image_dict["border.left"], (0, 20))
        self.screen.blit(self.image_dict["border.right"], (self.parent.screen_dim[0]-20, 20))
        self.screen.blit(self.image_dict["border.top"], (20, 0))
        self.screen.blit(self.image_dict["border.bottom"], (20, self.parent.screen_dim[1]-20))

        # the corners
        self.screen.blit(self.image_dict["corner"], (0, 0))
        self.screen.blit(self.image_dict["corner"], (self.parent.screen_dim[0]-20, 0))
        self.screen.blit(self.image_dict["corner"], (0, self.parent.screen_dim[1]-20))
        self.screen.blit(self.image_dict["corner"], (self.parent.screen_dim[0]-20, self.parent.screen_dim[1]-20))

        # the title bar,text,box,minibox,  ... in that order
        self.screen.blit(self.title_bar, (20, 20))
        self.screen.blit(self.title[0], ((20+4 + (self.parent.screen_dim[0]-40))/2-self.title[1]/2, 20+4))
        self.screen.blit(self.box, (self.parent.map.window_w*20, 45))
        self.screen.blit(self.mini_box, (self.parent.map.window_w*20+6, 45+8))

        # mini_map
        self.screen.blit(self.mini_map, (self.parent.map.window_w*20+6+4, 45+8+4))
        x, y = self.parent.map.cur_pos
        w, h = self.parent.map.window_w, self.parent.map.window_h
        x, y, w, h = x * 1.6, y * 1.6, w * 1.6, h * 1.6
        pygame.draw.rect(self.screen, (200, 200, 200), (x + self.parent.map.window_w*20+6+4, y + 45+8+4, w, h), 1)

        # money(gold) amount
        self.screen.blit(self.gold_image, (self.parent.map.window_w*20+6, 45+8+179))
        text = self.big_font.render(str(self.parent.human.money), 1, (30, 30, 30))
        self.screen.blit(text, (self.parent.map.window_w*20 + self.gold_image.get_width()+10, 45+8+178+3))

        # power
        self.screen.blit(self.power_image, (self.parent.map.window_w*20+6+10+75, 45+8+174))
        text = self.medium2_font.render("R: "+str(self.parent.human.req_power), 1, (30, 30, 30))
        self.screen.blit(text, (self.parent.map.window_w*20+6 + self.gold_image.get_width()+25+60, 45+9+173))
        text = self.medium2_font.render("H: "+str(self.parent.human.power), 1, (30, 30, 30))
        self.screen.blit(text, (self.parent.map.window_w*20+6 + self.gold_image.get_width()+25+60, 45+9+193))

        # context box
        h = self.mini_box.get_height() + self.gold_image.get_height() + 10 + 10
        self.screen.blit(self.context_box, (self.parent.map.window_w*20+6, 45+8 + h))

        # Selection box
        self.mouse_pos = pygame.mouse.get_pos()
        right_of_the_left_end = self.parent.map.x0 <= self.mouse_pos[0]
        left_of_the_right_end = self.mouse_pos[0] <= self.parent.map.x1
        below_the_top = self.parent.map.y0 <= self.mouse_pos[1]
        above_the_bottom = self.mouse_pos[1] <= self.parent.map.y1
        mouse_inside_the_play_space = right_of_the_left_end and left_of_the_right_end and below_the_top \
            and above_the_bottom
        self.c = list(pygame.mouse.get_pos())
        if not mouse_inside_the_play_space:
            if not above_the_bottom:
                self.c[1] = self.parent.map.y1-5
            if not below_the_top:
                self.c[1] = self.parent.map.y0+1
            if not right_of_the_left_end:
                self.c[0] = self.parent.map.x0+1
            if not left_of_the_right_end:
                self.c[0] = self.parent.map.x1-1
        if self.dragging == 1:
            print self.drag_start
            if self.parent.map.x0 <= self.drag_st_x <= self.parent.map.x1 and \
                    self.parent.map.y0 <= self.drag_st_y <= self.parent.map.y1:
                print self.drag_st_x, self.drag_st_y, self.c[0]-self.drag_st_x, self.c[1]-self.drag_st_y

                pygame.draw.rect(self.screen, (100, 255, 255), (self.drag_st_x, self.drag_st_y,
                                                                self.c[0]-self.drag_st_x, self.c[1]-self.drag_st_y), 1)
                x0, y0 = self.conv(self.drag_st_x, self.drag_st_y)
                x1, y1 = self.conv(self.c[0], self.c[1])
                self.parent.game_data.select_units(x0, y0, x1, y1, self.parent.human)

        # Selected object data
        x, y = self.parent.map.window_w*20+6, 45+8+h

        self.coord_of_the_sel_data_box = pygame.Rect(x, y, self.context_box.get_width(), self.context_box.get_height())

        nx, ny = x + 58, y + 20                                 # x + 20 + 20 + 10, y + 10
        hx, hy = self.conv(*pygame.mouse.get_pos())

        if self.multiple_selected:
            startx, starty, padx, pady = nx-45, ny-8, 5, 5
            number = len(self.multiple_selected)
            # numx, numy = number % 3,  number / 3
            # print numx, numy
            dx, dy = 0, 0
            pos = 0
            for imaager in self.image_for_selection:
                lx, ly = startx + padx*dx + 40*dx, starty + pady*dy + dy*40
                self.multi_sel_image_init_points.append(((lx, ly), self.multiple_selected[pos][0]))
                self.screen.blit(imaager, (lx, ly))
                dx += 1
                if dx == 3:
                    dx = 0
                    dy += 1
                pos += 1
            pass
        elif self.selected_unit:
            text = self.medium_font.render(self.selected_unit.name, 1, (30, 30, 30), (128, 160, 192))
            self.screen.blit(text, (nx-7, ny-10))
            self.screen.blit(self.image_for_selection, (nx-50, ny-13))

            # health bar
            ax, ay, aw, ah = nx-5, ny+7, 102, 15
            pygame.draw.rect(self.screen, (10, 10, 10), (ax, ay, aw, ah), 1)
            health, thealth = self.selected_unit.health, self.selected_unit.total_health
            percent = (health * 100) / thealth
            pygame.draw.rect(self.screen, (10, 10, 10), (ax, ay, aw, ah), 1)
            pygame.gfxdraw.box(self.screen, (ax+1, ay+1, percent, ah-2), (150, 50, 50))

            # task doing
            zx, zy, zw, zh = ax-40, ay+132, aw+40, ah+2
            pygame.draw.rect(self.screen, (10, 10, 10), (zx, zy, zw, zh), 2)
            if not self.selected_unit.idle:
                filled = self.selected_unit.task_done / 100.0 * zw - 3
                pygame.gfxdraw.box(self.screen, (zx+2, zy+2, filled, zh-3), (100, 100, 130))
            else:
                tmage = self.small_font.render("unit is idle", 1, (30, 30, 30), (128, 160, 192))
                ix, iy = (2*zx + zw) / 2 - tmage.get_width()/2, zy + 3
                self.screen.blit(tmage, (ix, iy))

        elif self.parent.map.x0 <= pygame.mouse.get_pos()[0] <= self.parent.map.x1 and \
                self.parent.map.y0 <= pygame.mouse.get_pos()[1] <= self.parent.map.y1:
            if self.parent.game_data.is_place_empty(hx, hy):
                terrain = self.parent.map.get_terrain_type(hx, hy)
                text = self.big_font.render(terrain[0], 1, (30, 30, 30), (128, 160, 192))
                self.screen.blit(text, (nx-20, ny))
            elif not self.parent.game_data.is_place_empty(hx, hy):
                text = self.medium2_font.render(self.parent.game_data.get_unit(hx, hy)[0].name, 1, (30, 30, 30),
                                                (128, 160, 192))

                self.screen.blit(text, (nx-40, ny))

        # for selection options
        if self.selected_options:
            pygame.gfxdraw.box(self.screen, (int(x+10), int(y+40+10), 150, 4), (50, 50, 50))
            fx, fy, fx1, fy1 = int(x+10), int(y+40+5)+15, 150, 95                 # value of 95 was 115
            pygame.draw.rect(self.screen, (100, 100, 100), (fx, fy, fx1, fy1), 3)
            dx, dy = int(fx + 10), int(fy + 10)

            p = 0
            self.selection_boxes_and_state = []
            for i in self.selected_options:
                name = i
                image = self.selected_options[i]
                text_surface = self.small_font.render(name, 1, (30, 30, 30), (128, 160, 192))
                textx, texty = dx+25, dy+int(text_surface.get_size()[1]*p)+9*p
                self.screen.blit(text_surface, (textx, texty))
                image = pygame.transform.scale(image, (20, 20))
                imagex, imagey = dx-2, dy+int(text_surface.get_size()[1]*p)-4 + 9*p
                self.screen.blit(image, (imagex, imagey))
                # txtsx, txtsy = text_surface.get_size()

                the_selection_area = pygame.Rect([imagex-2, imagey, 140, image.get_size()[1]])
                self.selection_boxes_and_state.append([the_selection_area, name, False])
                pygame.draw.rect(self.screen, (100, 100, 100), the_selection_area, 1)
                p += 1
        elif self.selected_unit:
            pygame.gfxdraw.box(self.screen, (int(x+10), int(y+40+10), 150, 4), (50, 50, 50))
            fx, fy, fx1, fy1 = int(x+10), int(y+40+5)+15, 150, 95
            pygame.draw.rect(self.screen, (100, 100, 100), (fx, fy, fx1, fy1), 3)

        self.process_events()
        self.popup_info()

        #######################################################################
        #################  for positioning  ###################################
        if isinstance(self.selected_unit,  unit_base.command_center) and self.selected_unit.positioning:
            self.mouse_pos = pygame.mouse.get_pos()

            x = (self.mouse_pos[0]-self.parent.map.x_offset)/20+self.parent.map.cur_pos[0]
            y = (self.mouse_pos[1]-self.parent.map.y_offset)/20+self.parent.map.cur_pos[1]
            dtx = (x - self.parent.map.cur_pos[0] + 1) * 20
            dty = (y - self.parent.map.cur_pos[1] + 2) * 20+5

            # self.placeable
            placeable = True
            for qy in range(3):
                for qx in range(2):
                    if not self.parent.game_data.is_place_truly_empty(x+qx, y+qy):
                        placeable = False
                        break
            if placeable:
                self.placeable = True
                self.screen.blit(self.grey_image, (dtx, dty))
            else:
                self.placeable = False
                self.screen.blit(self.red_image, (dtx, dty))

        #######################################################################
        self.map_panning_mouse()

        if not self.game_area.collidepoint(pygame.mouse.get_pos()):
            self.current_cursor = self.cursor_images["default"]
        self.screen.blit(self.current_cursor, pygame.mouse.get_pos())

        # print (pygame.time.get_ticks() - qqq)

    def process_events(self):
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key in self.q:
                    self.q[event.key][0](self.q[event.key][1], self.q[event.key][2])
            elif event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.left_mouse_clicked = 1
                elif event.button == 2:
                    self.middle_mouse_clicked = 1
                elif event.button == 3:
                    self.right_mouse_clicked = 1
                self.drag_start = 0
                # in the box where the data on selected items appear
                if self.coord_of_the_sel_data_box.collidepoint(event.pos):
                    mx, my = event.pos
                    if self.multiple_selected:
                        for h in self.multi_sel_image_init_points:
                            if Rect(h[0][0], h[0][1], 40, 40).collidepoint(mx, my):
                                self.parent.game_data.selected = h[1]
                                self.multiple_selected = False
                                self.selected_unit = h[1]
                                self.image_for_selection = h[1].selection_image
                                self.selected_options = h[1].selection_options
                        pass
                    elif self.selected_unit:
                        for area in self.selection_boxes_and_state:
                            if area[0].collidepoint(mx, my):
                                self.selected_unit.do_selection(area[1])
                                break
                        pass
                    else:
                        pass
                # inside the game space
                elif self.parent.map.x0 <= event.pos[0] <= self.parent.map.x1 and \
                        self.parent.map.y0 <= event.pos[1] <= self.parent.map.y1 and \
                        event.button == 1:       # inside the game area
                    x = (self.mouse_pos[0]-self.parent.map.x_offset)/20+self.parent.map.cur_pos[0]
                    y = (self.mouse_pos[1]-self.parent.map.y_offset)/20+self.parent.map.cur_pos[1]

                   # for command center placing units
                    if isinstance(self.selected_unit, unit_base.command_center) and self.selected_unit.positioning:
                            if self.placeable:
                                self.selected_unit.place_pos = x, y
                                self.selected_unit.positioning_completed()
                            else:
                                self.parent.message.put_message("The building can't be placed there")
                    else:
                        # Unit selection
                        sel_unit = self.parent.game_data.select_unit(x, y, self.parent.human)
                        if sel_unit:
                            self.multiple_selected = False
                            self.selected_unit = sel_unit[0]
                            self.image_for_selection = sel_unit[0].selection_image
                            self.selected_options = sel_unit[0].selection_options
                        else:
                            self.multiple_selected = False
                            self.selected_unit = False
                            self.image_for_selection = None
                            self.selected_options = []
                elif self.parent.map.x0 <= event.pos[0] <= self.parent.map.x1 and \
                        self.parent.map.y0 <= event.pos[1] <= self.parent.map.y1 and \
                        event.button == 3:                     # same as above ,right click.
                    if self.selected_unit:
                        # print self.parent.pathfinder.get_path((20, 9), (22, 12))
                        self.selected_unit.right_click_handle(*self.conv(event.pos[0], event.pos[1]))
                        pass
                    elif self.multiple_selected:
                        pass
            elif event.type == MOUSEBUTTONUP:
                if self.drag_start:
                    self.drag_end = event.pos
                    self.dragging = 0
                if event.button == 1:
                    self.left_mouse_clicked = 0
                elif event.button == 2:
                    self.middle_mouse_clicked = 0
                elif event.button == 3:
                    self.right_mouse_clicked = 0
                if self.drag_start:
                    x0, x1 = [[self.drag_start[0], self.drag_end[0]],
                              [self.drag_end[0], self.drag_start[0]]][self.drag_start[0] >= self.drag_end[0]]
                    y0, y1 = [[self.drag_start[1], self.drag_end[1]],
                              [self.drag_end[1], self.drag_start[1]]][self.drag_start[1] >= self.drag_end[1]]

                    sel = self.parent.game_data.select_units(x0, y0, x1, y1, self.parent.human)

                    if not sel:
                        self.multiple_selected = False
                        self.selected_unit = False
                        self.image_for_selection = None
                        self.selected_options = []
                    elif len(sel) == 1:
                        self.multiple_selected = False
                        self.selected_unit = sel[0][0]
                        self.image_for_selection = sel[0][0].selection_image
                        self.selected_options = sel[0][0].selection_options
                    else:
                        self.multiple_selected = sel[:9]
                        self.selected_unit = False
                        self.image_for_selection = [f[0].selection_image for f in self.multiple_selected]
                        # print self.image_for_selection
                        self.selected_options = None
            elif event.type == MOUSEMOTION:
                self.mouse_pos = pygame.mouse.get_pos()
                self.time_last_moved = pygame.time.get_ticks()
                if event.buttons == (1, 0, 0):
                    if self.dragging == 0:
                        self.drag_start = self.drag_st_x, self.drag_st_y = (event.pos[0]+event.rel[0],
                                                                            event.pos[1]+event.rel[1])
                        self.dragging = 1

    def map_panning_mouse(self):
        if (pygame.time.get_ticks() - self.time_last_map_moved) > 70:
            x, y = self.mouse_pos
            # left
            if 0 <= x <= 20:
                self.parent.map.move_pos(-1, 0)
            if 0 <= y <= 20:
                self.parent.map.move_pos(0, -1)
            if (self.parent.screen_dim[0]-20) <= x <= self.parent.screen_dim[0]:
                self.parent.map.move_pos(+1, 0)
            if (self.parent.screen_dim[1]-20) <= y <= self.parent.screen_dim[1]:
                self.parent.map.move_pos(0, +1)
            self.time_last_map_moved = pygame.time.get_ticks()

    def popup_info(self):
        if (pygame.time.get_ticks() - self.time_last_moved) > 700:
            if self.parent.map.x_offset < self.mouse_pos[0] < self.parent.map.x_offset + \
                    (self.parent.map.window_w-1)*20 and self.parent.map.y_offset < self.mouse_pos[1] \
                    < self.parent.map.y_offset + (self.parent.map.window_h-2)*20:
                x, y = (self.mouse_pos[0]-self.parent.map.x_offset)/20, (self.mouse_pos[1]-self.parent.map.y_offset)/20
                if self.parent.game_data.is_place_empty(x, y):
                    x = (self.mouse_pos[0]-self.parent.map.x_offset)/20+self.parent.map.cur_pos[0]
                    y = (self.mouse_pos[1]-self.parent.map.y_offset)/20+self.parent.map.cur_pos[1]

                    s = self.parent.map.get_terrain_type(x, y)

                    text = self.small_font.render(s[0].capitalize(), 1, (0, 0, 0), (198, 253, 96))
                    board = pygame.Surface((text.get_width()+8,  text.get_height()+5))
                    board.fill((198, 253, 96))

                    pygame.draw.rect(board, (0, 0, 0), (0, 0, text.get_width()+8, text.get_height()+9), 1)
                    board.blit(text, ((6+text.get_width())/2-text.get_width()/2,
                                      4+text.get_height()/2-text.get_height()/2))

                    self.screen.blit(board,(self.mouse_pos[0], self.mouse_pos[1]-board.get_height()-3))