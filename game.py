import pygame
from pygame.locals import *
import config as c
import sys

from collections import defaultdict


class Game:
    def __init__(self, caption, back_image_filename, frame_rate):
        self.background_image = pygame.image.load(back_image_filename)
        self.frame_rate = frame_rate
        self.game_over = False
        self.objects = []

        pygame.mixer.init(44100, -16, 2, 4096)
        pygame.init()
        pygame.font.init()

        c.screen_width = pygame.display.Info().current_w
        c.screen_height = pygame.display.Info().current_h

        self.surface = pygame.display.set_mode((c.screen_width, c.screen_height), FULLSCREEN)

        pygame.display.set_caption(caption)
        self.clock = pygame.time.Clock()

        self.keydown_handlers = defaultdict(list)
        self.keyup_handlers = defaultdict(list)
        self.mouse_handlers = []

        self.keydown_handlers[pygame.K_ESCAPE].append(self.quit_game)

    def update(self):
        for o in self.objects:
            o.update()

    def draw(self):
        for o in self.objects:
            o.draw(self.surface)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # "close window" button
                self.quit_game()
            elif event.type == pygame.KEYDOWN:
                for handler in self.keydown_handlers[event.key]:
                    handler(event.key)
            elif event.type == pygame.KEYUP:
                for handler in self.keyup_handlers[event.key]:
                    handler(event.key)
            elif event.type in (pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP, pygame.MOUSEMOTION):
                for handler in self.mouse_handlers:
                    handler(event.type, event.pos)

    @staticmethod
    def quit_game(_):
        pygame.quit()
        sys.exit()

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
        # self.leaderboard()
