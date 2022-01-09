from pygame.rect import Rect
import config as c


class GameObject:
    def __init__(self, x, y, w, h, speed=(0, 0)):
        self._rect = Rect(x, y, w, h)
        self._speed = (round(speed[0] * c.speed_scale), round(speed[1] * c.speed_scale))

    @property
    def rect(self):
        return self._rect

    @property
    def speed(self):
        return self._speed

    def draw(self, surface):
        pass

    def move(self, dx, dy):
        self._rect = self._rect.move(dx, dy)

    def update(self):
        """"""
        if self._speed == [0, 0]:
            return

        self.move(*self._speed)
