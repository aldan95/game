import pygame

from game_object import GameObject
import config as c

class Boss(GameObject):

    def __init__(self, image, x, y, hp):
        self.image_surface = pygame.image.load('images/boss1.png').convert_alpha()
        self.image_damage = pygame.image.load('images/boss1damage.png').convert_alpha()
        self._boom = False
        self._damage = False
        self.hp = 10
        self.x = c.screen_width
        self.y = c.screen_height/2
        self.switcher = True
        self.introduction_damage = True #переменная чтобы хитбокс работал нормально когда он выезжает
        self.bullet_delay = 0
        self.bullet_delay_next = 20
        rect = self.image_surface.get_rect()
        GameObject.__init__(self, x + rect.left, y + rect.top, rect.width, rect.height)

    def boom(self):
        self._boom = True

    def boomed(self):
        return self._boom

    def damage(self):
        self._damage = True

    def draw(self, surface):
        if self._boom:
            surface.blit(self.boom_surface, (self.rect.left, self.rect.top))
        elif self._damage:
            surface.blit(self.image_damage, (self.rect.left, self.rect.top))
        else:
            surface.blit(self.image_surface, (self.rect.left, self.rect.top))

    def update(self):
        if not self._boom:
            if self.x > c.screen_width-200:
                self.move(-1, 0)
                self.x -= 1
            else:
                self.introduction_damage = False
                if self.y == 600:
                    self.switcher = False
                if self.y == 150:
                    self.switcher = True
                if self.y < 600 and self.switcher:
                    self.move(0, -1)
                    self.y += 1
                if self.y > 150 and not self.switcher:
                    self.move(0, 1)
                    self.y -= 1

        self.fire = False

