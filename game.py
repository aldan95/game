import pygame
from pygame.locals import *
import config as c
import sys
from text_object import TextObject
from button import Button
from collections import defaultdict


class Game:
    def __init__(self, caption, width, height, back_image_filename, frame_rate):
        self.background_image = pygame.image.load(back_image_filename)
        self.frame_rate = frame_rate
        self.game_over = False
        self.objects = []
        self.pause = True
        pygame.mixer.init(44100, -16, 2, 4096)
        pygame.init()
        pygame.font.init()
        self.surface = pygame.display.set_mode((width, height), FULLSCREEN)
        #self.surface = pygame.display.set_mode((width, height))
        pygame.display.set_caption(caption)
        self.clock = pygame.time.Clock()
        self.keydown_handlers = defaultdict(list)
        self.keyup_handlers = defaultdict(list)
        self.mouse_handlers = []

    def update(self):
        for o in self.objects:
            o.update()

    def draw(self):
        for o in self.objects:
            o.draw(self.surface)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE and not self.pause:

                    self.pause_message = TextObject(c.screen_width/2-60,
                                                  c.screen_height/2-100,
                                                  lambda: f'GAME PAUSED',
                                                  c.text_color,
                                                  c.font_name,
                                                  c.font_size)
                    self.objects.append(self.pause_message)

                    self.pause = True

                    def on_mm(_):
                        self.objects.remove(self.pause_message)
                        self.pause = True
                        self.start_level = False
                        self.is_game_running_normal = False
                        self.is_game_running_boss = False
                        self.create_menu()
                        return


                    def on_quit(_):
                        pygame.quit()
                        sys.exit()

                    self.menu_buttons.clear()
                    for i, (text, click_handler) in enumerate(
                            (('MAIN MENU', on_mm), ('QUIT', on_quit))):
                        b = Button((c.screen_width - c.menu_button_w) // 2 - 45,
                                   # -45 чтобы было ровно по центру по горизонтали
                                   c.menu_offset_y + (c.menu_button_h + 5) * i - 30,
                                   # -30 чтобы было ровно по центру по вертикали
                                   c.menu_button_w + 90,
                                   c.menu_button_h,
                                   text,
                                   click_handler,
                                   padding=5)
                        self.objects.append(b)
                        self.menu_buttons.append(b)
                        self.mouse_handlers.append(b.handle_mouse_event)




                elif event.key == pygame.K_ESCAPE and self.pause:
                    self.pause = False
                    self.objects.remove(self.pause_message)
                    for b in self.menu_buttons:
                        self.objects.remove(b)
                    self.menu_buttons.clear()
                    self.mouse_handlers.clear()

                for handler in self.keydown_handlers[event.key]:
                    handler(event.key)
            elif event.type == pygame.KEYUP:
                for handler in self.keyup_handlers[event.key]:
                    handler(event.key)
            elif event.type in (pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP, pygame.MOUSEMOTION):
                for handler in self.mouse_handlers:
                    handler(event.type, event.pos)


    def leaderboard(self):  # функция написана в breakout, но вызывается здесь
        pass

    def run(self):
        while not self.game_over:
            self.surface.blit(self.background_image, (0, 0))

            self.handle_events()
            self.update()
            self.draw()

            pygame.display.update()
            self.clock.tick(self.frame_rate)
        #self.leaderboard()
