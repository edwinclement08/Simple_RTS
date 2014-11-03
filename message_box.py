__author__ = 'Edwin Clement'
import pygame, sys, pygame.gfxdraw
if not pygame.font:
    print 'Warning, fonts disabled'


class Message:
    def __init__(self, w, h):
        self.screen = pygame.Surface((w, h))
        self.screen.set_colorkey((0, 0, 0))

        self.big_font = pygame.font.Font(None, 29)
        self.font = pygame.font.Font(None, 22)
        self.text_image = None
        self.message_box = None
        self.title_image = None
        self.text = ""

        self.time = 1000
        self.time_started = None
        self.title = "Attention!!"
        self.fg = (10, 10, 10)
        self.bg = (56, 56, 65)

        self.working = False

    def put_message(self, text, **kwargs):
        d = kwargs

        if "time" in d:
            self.time = d["time"]
        else:
            self.time = 2000

        if "fg" in d:
            self.fg = d["fg"]
        else:
            self.fg = (10, 10, 10)

        if "title" in d:
            self.title = d["title"]
        else:
            self.title = "Attention!!"

        if "bg" in d:
            self.bg = d["bg"]
        else:
            self.bg = (56, 56, 65)

        self.text = text

        self.title_image = self.big_font.render(self.title, 1, self.fg, self.bg)
        self.text_image = self.font.render(self.text, 1, self.fg, self.bg)

        w = self.font.size(self.text)[0] + self.big_font.size(self.title)[0] + 20
        h = self.font.size(self.text)[1] + self.big_font.size(self.title)[1] + 30

        self.message_box = pygame.Surface((w, h))
        self.message_box.fill(self.bg)

        tx = w/2-self.title_image.get_width()/2
        ty = self.title_image.get_height()/2 + 3
        mx = w/2-self.text_image.get_width()/2
        my = self.text_image.get_height()/2 + 30

        self.message_box.blit(self.title_image, (tx, ty))
        self.message_box.blit(self.text_image, (mx, my))

        self.time_started = pygame.time.get_ticks()
        self.working = True
        self.update()

    def update(self):
        if self.working:
            if pygame.time.get_ticks() - self.time_started >= self.time:
                self.screen.fill((0,0,0))
                self.working = False
                self.time = 2000
                self.time_started = None
                self.title = "Attention!!"
                self.fg = (0, 0, 0)
                self.bg = (255, 255, 255)
            else:
                x = 200
                y = 370
                self.screen.blit(self.message_box, (x, y))