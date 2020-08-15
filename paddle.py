import pygame

import config as c
from game_object import GameObject


class Paddle(GameObject):
    def __init__(self, x, y, w, h, color, offset):
        GameObject.__init__(self, x, y, w, h)
        self.color = color
        self.offset = offset
        self.moving_left = False
        self.moving_right = False

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self._rect)

    def handle(self, key):
        if key == pygame.K_LEFT:
            self.moving_left = not self.moving_left
        else:
            self.moving_right = not self.moving_right

    def update(self):
        if self.moving_left:
            dx = -(min(self.offset, self.rect.left))
        elif self.moving_right:
            dx = min(self.offset, c.screen_width - self.rect.right)
        else:
            return

        self.move(dx, 0)
