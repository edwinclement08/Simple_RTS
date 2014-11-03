__author__ = 'Edwin Clement'
import json,pygame
if not pygame.font: print 'Warning, fonts disabled'

class Interface:
        data_file = "interface.json"
        image_file = "interface.bmp"
        title_file = "title_bar.bmp"
        box_file = "box.bmp"

        def __init__(self,parent):
            self.parent = parent
            self.screen = pygame.Surface(parent.screen_dim).convert()
            self.screen.fill((255,255,255))
            self.screen.set_colorkey((255,255,255))

            self.title_bar = pygame.image.load(self.title_file).convert()
            self.box = pygame.image.load(self.box_file).convert()

            pic_data = json.load(open(self.data_file))
            self.mother_of_images = pygame.image.load(self.image_file).convert()
            self.main_pixel_array = mpa = pygame.PixelArray(self.mother_of_images)
            self.image_dict = {}
            for m in pic_data:
                if m == "transparent_color":
                    continue
                x1, y1, x2, y2 = pic_data[m]
                sub_image = mpa[x1:x2,y1:y2]
                self.image_dict[m] = sub_image.make_surface()


            self.font = pygame.font.Font(None, 26)
            text = self.font.render("The Game v1.0", 1, (10, 10, 10))
            w,h = text.get_width(), text.get_height()
            self.title = text, w, h


            self.update()


        def update(self):
            # the borders
            self.screen.blit(self.image_dict["border.left"], (0, 20))
            self.screen.blit(self.image_dict["border.right"], (self.parent.screen_dim[0]-20, 20))
            self.screen.blit(self.image_dict["border.top"], (20, 0))
            self.screen.blit(self.image_dict["border.bottom"], (20, self.parent.screen_dim[1]-20))

            # the corners
            self.screen.blit(self.image_dict["corner"],(0,0))
            self.screen.blit(self.image_dict["corner"],(self.parent.screen_dim[0]-20,0))
            self.screen.blit(self.image_dict["corner"],(0,self.parent.screen_dim[1]-20))
            self.screen.blit(self.image_dict["corner"],(self.parent.screen_dim[0]-20,self.parent.screen_dim[1]-20))

            # the title bar,text,box
            self.screen.blit(self.title_bar,(20,20))
            self.screen.blit(self.title[0],((20+4 + (self.parent.screen_dim[0]-40))/2-self.title[1]/2,20+4))
            self.screen.blit(self.box,(self.parent.map.window_w*20,45))


            # remaining area
            # x = self.parent.screen_dim[0] - self.parent.map.window_w*20 - 20
            # y = self.parent.screen_dim[1] - 40

            print self.parent.screen_dim[0] - self.parent.map.window_w*20 - 40
            print self.parent.screen_dim[1] - 40




#
# pygame.init()
# screen = pygame.display.set_mode((800,600))
#
# class garbage():
#     screen_dim = 800,600
#
# e = Interface(garbage())
# screen.blit(e.screen,(0,0))
# pygame.display.update()
# while 1:
#     pass
# pygame.quit()