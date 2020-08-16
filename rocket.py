import pygame

import config as c
from game_object import GameObject


class Rocket(GameObject):

    def __init__(self, x, y):
        # https://younglinux.info/pygame/image
        self.image_surface = pygame.image.load('images/rocket.png').convert_alpha()
        #self.image_surface.set_colorkey((255, 255, 255, 255))
        rect = self.image_surface.get_rect()
        GameObject.__init__(self, x + rect.left, y + rect.top, rect.width, rect.height)
        self.dy = 0
        self.fire = False
        return

    def draw(self, surface):
        surface.blit(self.image_surface, (self.rect.left, self.rect.top))

    def handle_down(self, key):
        if key == pygame.K_UP:
            self.dy = -1
        elif key == pygame.K_DOWN:
            self.dy = 1
        elif key == pygame.K_SPACE:
            self.fire = True

    def handle_up(self, key):
        if key == pygame.K_SPACE:
            self.fire = False
        else:
            self.dy = 0

    def update(self):
        self.move(0, self.dy)
        if self.fire:
            print('firing...')
