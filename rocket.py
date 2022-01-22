import pygame
import os
import config as c
from game_object import GameObject

assert os.path.isfile('sound_effects/brick_hit.wav')

class Rocket(GameObject):

    def __init__(self, x, y):
        # https://younglinux.info/pygame/image
        self.sound_effects = {name: pygame.mixer.Sound(sound) for name, sound in c.sounds_effects.items()}
        self.image_surface = pygame.image.load('images/rocket.png').convert_alpha()
        self.boom_surface = pygame.image.load('images/rocket_boom.png').convert_alpha()
        # self.image_surface.set_colorkey((255, 255, 255, 255))
        rect = self.image_surface.get_rect()
        GameObject.__init__(self, x + rect.left, y + rect.top, rect.width, rect.height)
        self.dy = 0
        self.dx = 0
        self.y = c.screen_height/2
        self.x = 0
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
            if not c.death_swing:
                if key == pygame.K_UP:
                    self.dy = -2
                elif key == pygame.K_DOWN:
                    self.dy = 2
                elif key == pygame.K_SPACE:
                    self.fire = True
                elif key == pygame.K_RIGHT:
                    self.dx = 2
                elif key == pygame.K_LEFT:
                    self.dx = -2
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
            if not c.death_swing:
                self.dy = 0
                self.dx = 0

    def update(self):
        if not self._boom:
            if not c.death_swing:
                if self.dy > 0 and self.y < 566:  # 9600 - высота текстуры ракеты
                    self.move(0, self.dy)
                    self.y += self.dy
                elif self.dy < 0 and self.y > 0:
                    self.move(0, self.dy)
                    self.y += self.dy
                if self.dx > 0 and self.x < 500:
                    self.move(self.dx, 0)
                    self.x += self.dx
                elif self.dx < 0 and self.x > 0:
                    self.move(self.dx, 0)
                    self.x += self.dx
            else:
                if self.dy > 0 and self.y < 566:
                    self.move(0, self.dy)
                    self.y += self.dy
                elif self.dy < 0 and self.y > 0:
                    self.move(0, self.dy)
                    self.y += self.dy
                elif self.y >= 566 or self.y <= 0:
                    self._boom = True
                    self.sound_effects['brick_hit'].play()
            self.fire = False
