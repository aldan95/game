import pygame
from game_object import GameObject

class Alien(GameObject):

    def __init__(self, x, y):
        # https://younglinux.info/pygame/image
        self.image_surface = pygame.image.load('images/rocket.png')
        self.image_surface.set_colorkey((255, 255, 255, 255))
        rect = self.image_surface.get_rect()
        GameObject.__init__(self, x + rect.left, y + rect.top, rect.width, rect.height)
        self.dy = 0
        self.fire = False
        return
