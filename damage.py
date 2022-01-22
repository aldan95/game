import pygame
from game_object import GameObject
import config as c
import boss


class Damage(GameObject):

    def __init__(self, x, y):
        self.image_surface = pygame.image.load(f'images/boss1damage.png')
        self.image_damage2 = pygame.image.load('images/boss2damaged.png')
        self.image_damage3 = pygame.image.load('images/boss3damaged.png')
        self.image_damage4 = pygame.image.load('images/boss4damaged.png')
        self.image_damage5 = pygame.image.load('images/boss5damaged.png')
        rect = self.image_surface.get_rect()
        GameObject.__init__(self, x + rect.left, y + rect.top, rect.width, rect.height)
        self.life = 5

    def draw(self, surface):
        surface.blit(self.image_surface, (self.rect.left, self.rect.top))

    def update(self):
        if self.life > 0:
            self.life = self.life - 1
        super().update()