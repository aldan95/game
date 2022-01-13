import pygame
import config as c
from game_object import GameObject


class Rocket(GameObject):

    def __init__(self, x, y):
        # https://younglinux.info/pygame/image
        self.image_surface = pygame.image.load('images/rocket.png').convert_alpha()
        self.boom_surface = pygame.image.load('images/rocket_boom.png').convert_alpha()
        # self.image_surface.set_colorkey((255, 255, 255, 255))
        rect = self.image_surface.get_rect()
        GameObject.__init__(self, x + rect.left, y + rect.top, rect.width, rect.height)
        self.dy = 0
        self.y = c.screen_height/2
        self.fire = False
        self._boom = False
        return

    def boom(self):
        self._boom = True

    @property
    def boomed(self):
        return self._boom

    def draw(self, surface):
        if self._boom:
            surface.blit(self.boom_surface, (self.rect.left, self.rect.top))
        else:
            surface.blit(self.image_surface, (self.rect.left, self.rect.top))

    def handle_down(self, key):
        if self._boom:
            self.dy = 0
            self.fire = False
        else:
            if key == pygame.K_UP:
                self.dy = -2
            elif key == pygame.K_DOWN:
                self.dy = 2
            elif key == pygame.K_SPACE:
                self.fire = True

    def handle_up(self, key):
        if key == pygame.K_SPACE:
            self.fire = False
        else:
            self.dy = 0


    def update(self):
        if not self._boom:
            if self.dy > 0 and self.y < 566:  # 9600 - высота текстуры ракеты
                self.move(0, self.dy)
                self.y += self.dy
            elif self.dy < 0 and self.y > 0:
                self.move(0, self.dy)
                self.y += self.dy
        self.fire = False
