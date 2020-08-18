import random
from datetime import datetime, timedelta

import os
import time
import pygame
from pygame.rect import Rect

import config as c
from button import Button
from game import Game
from rocket import Rocket
from alien import Alien
from bullet import Bullet
from boom import Boom
from text_object import TextObject
import colors

assert os.path.isfile('sound_effects/brick_hit.wav')

class Breakout(Game):
    def __init__(self):
        Game.__init__(self, 'Space Insiders', c.screen_width, c.screen_height, c.background_image, c.frame_rate)
        self.sound_effects = {name: pygame.mixer.Sound(sound) for name, sound in c.sounds_effects.items()}
        self.reset_effect = None
        self.effect_start_time = None
        self.score = 0
        self.lives = c.initial_lives
        self.start_level = False
        self.alien_count = 3
        self.aliens_to_pass = self.alien_count * 3
        self.rocket = None
        self.menu_buttons = []
        self.is_game_running = False
        self.aliens = []
        self.bullets = []
        self.booms = []
        self.create_objects()
        self.screen = Rect(0, 0, c.screen_width, c.screen_height)

    def add_life(self):
        self.lives += 1

    def create_menu(self):
        def on_play(_):
            for b in self.menu_buttons:
                self.objects.remove(b)

            self.is_game_running = True
            self.start_level = True

        def on_quit(_):
            self.game_over = True
            self.is_game_running = False
            self.game_over = True

        for i, (text, click_handler) in enumerate((('PLAY', on_play), ('QUIT', on_quit))):
            b = Button((c.screen_width - c.menu_button_w) / 2,
                       c.menu_offset_y + (c.menu_button_h + 5) * i,
                       c.menu_button_w,
                       c.menu_button_h,
                       text,
                       click_handler,
                       padding=5)
            self.objects.append(b)
            self.menu_buttons.append(b)
            self.mouse_handlers.append(b.handle_mouse_event)

    def create_objects(self):
        self.create_labels()
        self.create_menu()
        self.create_rocket()
        for i in range(1, self.alien_count):
            self.create_alien()

    def create_labels(self):
        self.score_label = TextObject(c.score_offset,
                                      c.status_offset_y,
                                      lambda: f'SCORE: {self.score}',
                                      c.text_color,
                                      c.font_name,
                                      c.font_size)
        self.objects.append(self.score_label)
        self.lives_label = TextObject(c.lives_offset,
                                      c.status_offset_y,
                                      lambda: f'LIVES: {self.lives}',
                                      c.text_color,
                                      c.font_name,
                                      c.font_size)
        self.objects.append(self.lives_label)

    def create_rocket(self):
        rocket = Rocket(0, c.screen_height/2)
        self.keydown_handlers[pygame.K_UP].append(rocket.handle_down)
        self.keydown_handlers[pygame.K_DOWN].append(rocket.handle_down)
        self.keydown_handlers[pygame.K_SPACE].append(rocket.handle_down)
        self.keyup_handlers[pygame.K_UP].append(rocket.handle_up)
        self.keyup_handlers[pygame.K_DOWN].append(rocket.handle_up)
        self.keyup_handlers[pygame.K_SPACE].append(rocket.handle_up)
        self.rocket = rocket
        self.objects.append(self.rocket)

    def create_alien(self):
        alien = Alien(c.screen_width-30, random.randint(0, c.screen_height - 40))
        self.aliens.append(alien)
        self.objects.append(alien)
        self.aliens_to_pass = self.aliens_to_pass - 1
        if self.aliens_to_pass == 0:
            self.alien_count = self.alien_count + 1
            self.aliens_to_pass = self.alien_count * 3

    def create_bullet(self):
        bullet = Bullet(self.rocket.rect.right, self.rocket.rect.top + self.rocket.rect.height/2)
        self.bullets.append(bullet)
        self.objects.append(bullet)

    def create_boom(self, x, y):
        boom = Boom(x, y)
        self.booms.append(boom)
        self.objects.append(boom)

    def update(self):
        if not self.is_game_running:
            return

        if self.start_level:
            self.start_level = False
            self.show_message('GET READY!', centralized=True)

        if not self.aliens:
            self.show_message('YOU WIN!!!', centralized=True)
            self.is_game_running = False
            self.game_over = True
            return

        # Reset special effect if needed
        if self.reset_effect:
            if datetime.now() - self.effect_start_time >= timedelta(seconds=c.effect_duration):
                self.reset_effect(self)
                self.reset_effect = None

        if self.rocket.fire:
            self.create_bullet()
        self.handle_aliens()
        super().update()

        if self.game_over:
            self.show_message('GAME OVER!', centralized=True)

    def handle_aliens(self):
        def intersect(s, a):
            return s.left < a.right and s.right > a.left and s.top < a.bottom and s.bottom > a.top

        if self.rocket.boomed:
            self.game_over = True
            return

        for alien in self.aliens:
            if not intersect(self.screen, alien.rect):
                self.objects.remove(alien)
                self.aliens.remove(alien)
            if intersect(self.rocket.rect, alien.rect):
                self.rocket.boom()
                self.sound_effects['brick_hit'].play()
                return

        if len(self.aliens) < self.alien_count:
            self.create_alien()
        for bullet in self.bullets:
            if intersect(self.screen, bullet.rect):
                for alien in self.aliens:
                    if intersect(alien.rect, bullet.rect):
                        self.create_boom(alien.rect.left, alien.rect.top)
                        self.objects.remove(bullet)
                        self.bullets.remove(bullet)
                        self.objects.remove(alien)
                        self.aliens.remove(alien)
                        self.sound_effects['brick_hit'].play()
                        break
            else:
                self.objects.remove(bullet)
                self.bullets.remove(bullet)
        for boom in self.booms:
            if boom.life <= 0:
                self.booms.remove(boom)
                self.objects.remove(boom)

    def show_message(self, text, color=colors.WHITE, font_name='Arial', font_size=20, centralized=False):
        message = TextObject(c.screen_width // 2, c.screen_height // 2, lambda: text, color, font_name, font_size)
        self.draw()
        message.draw(self.surface, centralized)
        pygame.display.update()
        time.sleep(c.message_duration)


def main():
    Breakout().run()


if __name__ == '__main__':
    main()
