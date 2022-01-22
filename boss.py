import pygame

from game_object import GameObject
import config as c

class Boss(GameObject):

    def __init__(self, x, y):
        self.image_surface = pygame.image.load('images/boss1.png').convert_alpha()
        self.image_surface2 = pygame.image.load('images/boss2.png').convert_alpha()
        self.image_surface3 = pygame.image.load('images/boss3.png').convert_alpha()
        self.image_surface4 = pygame.image.load('images/boss4.png').convert_alpha()
        self.image_surface5 = pygame.image.load('images/boss5.png').convert_alpha()

        self._boom = False
        self._damage = False
        self.hp = 10
        self.x = c.screen_width
        self.y = c.screen_height/2
        self.switcher = True
        self.introduction_damage = True  # переменная чтобы хитбокс работал нормально когда он выезжает
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


        elif self.hp > (c.boss_hp/5)*4:
            surface.blit(self.image_surface, (self.rect.left, self.rect.top))
        elif (c.boss_hp / 5)*4 >= self.hp > (c.boss_hp / 5)*3:
            surface.blit(self.image_surface2, (self.rect.left, self.rect.top))
        elif (c.boss_hp / 5)*3 >= self.hp > (c.boss_hp / 5)*2:
            surface.blit(self.image_surface3, (self.rect.left, self.rect.top))
        elif (c.boss_hp / 5)*2 >= self.hp > (c.boss_hp / 5):
            surface.blit(self.image_surface4, (self.rect.left, self.rect.top))
        elif self.hp <= c.boss_hp / 5:
            surface.blit(self.image_surface5, (self.rect.left, self.rect.top))


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

