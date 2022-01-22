import pygame
from game_object import GameObject


class Boom(GameObject):

    def __init__(self, x, y):
        self.image_surface = pygame.image.load(f'images/boom.png')
        self.image_surface1 = pygame.image.load(f'images/boom1.png')
        self.image_surface2 = pygame.image.load(f'images/boom2.png')
        self.image_surface3 = pygame.image.load(f'images/boom3.png')
        self.image_surface4 = pygame.image.load(f'images/boom4.png')
        self.image_surface5 = pygame.image.load(f'images/boom5.png')

        rect = self.image_surface.get_rect()
        GameObject.__init__(self, x + rect.left, y + rect.top, rect.width, rect.height)
        self.life = 25

    def draw(self, surface):
        if self.life > 20:
            surface.blit(self.image_surface1, (self.rect.left, self.rect.top))
        elif self.life > 15 and self.life <= 20:
            surface.blit(self.image_surface2, (self.rect.left, self.rect.top))
        elif self.life <= 15 and self.life > 10:
            surface.blit(self.image_surface3, (self.rect.left, self.rect.top))
        elif self.life > 5 and self.life <= 10:
            surface.blit(self.image_surface4, (self.rect.left, self.rect.top))
        elif self.life <= 5:
            surface.blit(self.image_surface5, (self.rect.left, self.rect.top))

    def update(self):
        if self.life > 0:
            self.life = self.life - 1
        super().update()
