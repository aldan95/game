import pygame
from game_object import GameObject


class Bullet(GameObject):

    def __init__(self, x, y):
        self.image_surface = pygame.image.load(f'images/bullet.png')
        rect = self.image_surface.get_rect()
        GameObject.__init__(self, x + rect.left, y + rect.top, rect.width, rect.height, (3, 0))

    def draw(self, surface):
        surface.blit(self.image_surface, (self.rect.left, self.rect.top))
