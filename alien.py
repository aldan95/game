import pygame
from game_object import GameObject


class Alien(GameObject):
    def __init__(self, image, x, y, speed):
        # https://younglinux.info/pygame/image
        self.image_surface = pygame.image.load(image)
        rect = self.image_surface.get_rect()
        GameObject.__init__(self, x + rect.left, y + rect.top, rect.width, rect.height, speed)
        '''(random.randint(-5, -1), 0)'''

    def draw(self, surface):
        surface.blit(self.image_surface, (self.rect.left, self.rect.top))


class AlienUfo(Alien):
    def __init__(self, x, y):
        Alien.__init__(self, "images/alien2.png", x, y, (-2, 0))


class AlienTriangle(Alien):
    def __init__(self, x, y):
        Alien.__init__(self, "images/alien1.png", x, y, (-1, 0))


class AlienMeteor(Alien):
    def __init__(self, x, y):
        Alien.__init__(self, "images/alien3.png", x, y, (-5, 0))


class AlienBug(Alien):
    def __init__(self, x, y):
        Alien.__init__(self, "images/alien4.png", x, y, (-4, 0))
