import pygame
from game_object import GameObject


class Damage(GameObject):

    def __init__(self, x, y):
        self.image_surface = pygame.image.load(f'images/boss1damage.png')
        rect = self.image_surface.get_rect()
        GameObject.__init__(self, x + rect.left, y + rect.top, rect.width, rect.height)
        self.life = 5

    def draw(self, surface):
        surface.blit(self.image_surface, (self.rect.left, self.rect.top))

    def update(self):
        if self.life > 0:
            self.life = self.life - 1
        super().update()