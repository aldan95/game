import pygame
import random
from game_object import GameObject


class Alien(GameObject):

    def __init__(self, x, y):
        # https://younglinux.info/pygame/image
        alienNo = random.randint(1, 3)
        self.image_surface = pygame.image.load(f'images/alien{alienNo}.png')
        rect = self.image_surface.get_rect()
        GameObject.__init__(self, x + rect.left, y + rect.top, rect.width, rect.height, (random.randint(-5, -1), 0))
        self.fire = False

    def draw(self, surface):
        surface.blit(self.image_surface, (self.rect.left, self.rect.top))
