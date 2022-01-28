import os
import random
import time
from datetime import datetime, timedelta

import pygame
from pygame.rect import Rect

import colors
import config as c
from alien import AlienBug
from alien import AlienMeteor
from alien import AlienTriangle
from alien import AlienUfo
from boom import Boom
from bullet import Bullet
from button import Button
from game import Game
from rocket import Rocket
from boss import Boss
from damage import Damage
from bossbullet import BossBullet
from text_object import TextObject

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
        self.alien_count = 2
        self.aliens_to_pass = self.alien_count * 3
        self.rocket = None
        self.menu_buttons = []
        self.is_game_running_normal = False
        self.is_game_running_boss = False
        self.aliens = []
        self.bullets = []
        self.booms = []
        self.damages = []
        self.boss_score = 50  # сколько очков нужно набрать чтобы появился босс
        self.boss_created = False
        self.boss_bullets = []
        self.boss = None
        self.boss_bullet_delay_next = 100
        self.create_objects()
        self.screen = Rect(0, 0, c.screen_width, c.screen_height)

    def add_life(self):
        self.lives += 1

    def create_menu(self):

        self.is_menu_message2 = False

        def on_play(_):

            if self.is_menu_message2:
                self.objects.remove(self.menu_message2)

            def on_standard_mode(_):

                self.objects.remove(self.menu_message)
                self.objects.append(self.menu_message2)
                self.is_menu_message2 = True

                def on_normal_survival(_):

                    self.objects.remove(self.menu_message2)
                    for b in self.menu_buttons:
                        self.objects.remove(b)
                    self.menu_buttons.clear()
                    self.mouse_handlers.clear()
                    self.is_game_running_normal = True
                    self.start_level = True
                    self.pause = False

                def on_boss_survival(_):

                    self.objects.remove(self.menu_message2)
                    for b in self.menu_buttons:
                        self.objects.remove(b)
                    self.menu_buttons.clear()
                    self.mouse_handlers.clear()
                    self.is_game_running_boss = True
                    self.start_level = True
                    self.pause = False

                for b in self.menu_buttons:
                    self.objects.remove(b)
                self.menu_buttons.clear()
                self.mouse_handlers.clear()

                for i, (text, click_handler) in enumerate(
                        (('NORMAL SURVIVAL', on_normal_survival),
                         ('BOSS SURVIVAL', on_boss_survival), ('BACK', on_play))):
                    b = Button((c.screen_width - c.menu_button_w) // 2 - 45,
                               # -45 чтобы было ровно по центру по горизонтали++++
                               c.menu_offset_y + (c.menu_button_h + 5) * i - 30,
                               # -30 чтобы было ровно по центру по вертикали
                               c.menu_button_w + 100,
                               c.menu_button_h,
                               text,
                               click_handler,
                               padding=5)
                    self.objects.append(b)
                    self.menu_buttons.append(b)
                    self.mouse_handlers.append(b.handle_mouse_event)

            def on_death_swing(_):

                self.objects.remove(self.menu_message)
                self.objects.append(self.menu_message2)
                c.death_swing = True

                def on_normal_survival(_):

                    self.objects.remove(self.menu_message2)
                    for b in self.menu_buttons:
                        self.objects.remove(b)
                    self.menu_buttons.clear()
                    self.mouse_handlers.clear()
                    self.is_game_running_normal = True
                    self.start_level = True
                    self.pause = False

                def on_boss_survival(_):

                    self.objects.remove(self.menu_message2)
                    for b in self.menu_buttons:
                        self.objects.remove(b)
                    self.menu_buttons.clear()
                    self.mouse_handlers.clear()
                    self.is_game_running_boss = True
                    self.start_level = True
                    self.pause = False

                for b in self.menu_buttons:
                    self.objects.remove(b)
                self.menu_buttons.clear()
                self.mouse_handlers.clear()

                for i, (text, click_handler) in enumerate(
                        (('NORMAL SURVIVAL', on_normal_survival),
                         ('BOSS SURVIVAL', on_boss_survival), ('BACK', on_play))):
                    b = Button((c.screen_width - c.menu_button_w) // 2 - 45,
                               # -45 чтобы было ровно по центру по горизонтали++++
                               c.menu_offset_y + (c.menu_button_h + 5) * i - 30,
                               # -30 чтобы было ровно по центру по вертикали
                               c.menu_button_w + 100,
                               c.menu_button_h,
                               text,
                               click_handler,
                               padding=5)
                    self.objects.append(b)
                    self.menu_buttons.append(b)
                    self.mouse_handlers.append(b.handle_mouse_event)

            def on_back(_):
                for b in self.menu_buttons:
                    self.objects.remove(b)
                self.menu_buttons.clear()
                self.mouse_handlers.clear()
                self.objects.remove(self.menu_message)
                self.create_menu()
                return

            for b in self.menu_buttons:
                self.objects.remove(b)
            self.menu_buttons.clear()
            self.mouse_handlers.clear()

            self.menu_message = TextObject(c.screen_width / 2 - 80,
                                            c.screen_height / 2 - 100,
                                            lambda: f'SELECT GAME MODE',
                                            c.text_color,
                                            c.font_name,
                                            c.font_size)

            self.menu_message2 = TextObject(c.screen_width / 2 - 90,
                                            c.screen_height / 2 - 100,
                                            lambda: f'SELECT SURVIVAL MODE',
                                            c.text_color,
                                            c.font_name,
                                            c.font_size)

            self.objects.append(self.menu_message)

            if self.objects.count(self.menu_message2) == 1:

                self.objects.remove(self.menu_message2)

            for i, (text, click_handler) in enumerate(
                    (('STANDARD MODE', on_standard_mode),
                     ('DEATH SWING MODE', on_death_swing), ('BACK', on_back))):
                b = Button((c.screen_width - c.menu_button_w) // 2 - 45,
                           # -45 чтобы было ровно по центру по горизонтали++++
                           c.menu_offset_y + (c.menu_button_h + 5) * i - 30,
                           # -30 чтобы было ровно по центру по вертикали
                           c.menu_button_w + 100,
                           c.menu_button_h,
                           text,
                           click_handler,
                           padding=5)
                self.objects.append(b)
                self.menu_buttons.append(b)
                self.mouse_handlers.append(b.handle_mouse_event)

            # for b in self.menu_buttons:
            #    self.objects.remove(b)

            # self.is_game_running = True
            # self.start_level = True

        def on_quit(_):
            self.game_over = True
            self.is_game_running = False

        for i, (text, click_handler) in enumerate((('PLAY', on_play), ('QUIT', on_quit))):
            b = Button((c.screen_width - c.menu_button_w) // 2,
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
            random1 = random.randint(1, 4)
            if random1 == 1:
                self.create_alien_ufo()
            if random1 == 2:
                self.create_alien_bug()
            if random1 == 3:
                self.create_alien_triangle()
            if random1 == 4:
                self.create_alien_meteor()
        # self.create_boss()

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
        rocket = Rocket(0, c.screen_height // 2)
        self.keydown_handlers[pygame.K_UP].append(rocket.handle_down)
        self.keydown_handlers[pygame.K_DOWN].append(rocket.handle_down)
        self.keydown_handlers[pygame.K_SPACE].append(rocket.handle_down)
        self.keydown_handlers[pygame.K_RIGHT].append(rocket.handle_down)
        self.keydown_handlers[pygame.K_LEFT].append(rocket.handle_down)
        self.keyup_handlers[pygame.K_UP].append(rocket.handle_up)
        self.keyup_handlers[pygame.K_DOWN].append(rocket.handle_up)
        self.keyup_handlers[pygame.K_SPACE].append(rocket.handle_up)
        self.keyup_handlers[pygame.K_RIGHT].append(rocket.handle_up)
        self.keyup_handlers[pygame.K_LEFT].append(rocket.handle_up)
        self.rocket = rocket
        self.objects.append(self.rocket)

    def create_boss(self):
        self.boss = Boss(c.screen_width, c.screen_height // 2)
        self.boss.hp = c.boss_hp
        self.objects.append(self.boss)
        self.boss._boom = False


    def create_alien_ufo(self):
        alien_ufo = AlienUfo(c.screen_width - 30, random.randint(0, c.screen_height - 40))
        self.aliens.append(alien_ufo)
        self.objects.append(alien_ufo)
        self.aliens_to_pass = self.aliens_to_pass - 1
        if self.aliens_to_pass == 0:
            self.alien_count = self.alien_count + 1
            self.aliens_to_pass = self.alien_count * 3

    def create_alien_triangle(self):
        alien_triangle = AlienTriangle(c.screen_width - 30, random.randint(0, c.screen_height - 40))
        self.aliens.append(alien_triangle)
        self.objects.append(alien_triangle)
        self.aliens_to_pass = self.aliens_to_pass - 1
        if self.aliens_to_pass == 0:
            self.alien_count = self.alien_count + 1
            self.aliens_to_pass = self.alien_count * 3

    def create_alien_bug(self):
        alien_bug = AlienBug(c.screen_width - 30, random.randint(0, c.screen_height - 40))
        self.aliens.append(alien_bug)
        self.objects.append(alien_bug)
        self.aliens_to_pass = self.aliens_to_pass - 1
        if self.aliens_to_pass == 0:
            self.alien_count = self.alien_count + 1
            self.aliens_to_pass = self.alien_count * 3

    def create_alien_meteor(self):
        alien_meteor = AlienMeteor(c.screen_width - 30, random.randint(0, c.screen_height - 40))
        self.aliens.append(alien_meteor)
        self.objects.append(alien_meteor)
        self.aliens_to_pass = self.aliens_to_pass - 1
        if self.aliens_to_pass == 0:
            self.alien_count = self.alien_count + 1
            self.aliens_to_pass = self.alien_count * 3

    def create_bullet(self):
        bullet = Bullet(self.rocket.rect.right, self.rocket.rect.top + self.rocket.rect.height // 2)
        self.bullets.append(bullet)
        self.objects.append(bullet)

    def create_boss_bullet(self):
        boss_bullet = BossBullet(self.boss.rect.left + 10, self.boss.rect.top + self.boss.rect.height // 2)
        self.boss_bullets.append(boss_bullet)
        self.objects.append(boss_bullet)

    def create_boom(self, x, y):
        boom = Boom(x, y)
        self.booms.append(boom)
        self.objects.append(boom)


#    def create_damage(self, x, y):
 #       damage = Boss.damage(x, y)
  #      self.damages.append(damage)
   #     self.objects.append(damage)

    def update(self):
        if self.pause:
            return

        if self.start_level:
            self.start_level = False
            self.show_message('GET READY!', centralized=True)

        '''if not self.aliens:
            self.show_message('YOU WIN!!!', centralized=True)    победа
            self.is_game_running = False
            self.game_over = True
            return'''

        # Reset special effect if needed
        if self.reset_effect:
            if datetime.now() - self.effect_start_time >= timedelta(seconds=c.effect_duration):
                self.reset_effect(self)
                self.reset_effect = None

        if self.rocket.fire:
            self.create_bullet()
        if not self.boss_created or self.boss._boom:
            self.handle_aliens()
        else:
            for alien in self.aliens:
                self.create_boom(alien.rect.left, alien.rect.top)
                self.objects.remove(alien)
                self.aliens.remove(alien)
                # self.score = self.score + 1
                self.sound_effects['brick_hit'].play()
                break

        if self.is_game_running_boss:
            if self.score >= self.boss_score and not self.boss_created:
                self.create_boss()
                self.boss_created = True
            elif self.score >= self.boss_score and self.boss_created:
                self.handle_boss()
                if not self.boss._boom and self.boss.bullet_delay < self.boss_bullet_delay_next:
                    self.boss.bullet_delay += 1
                elif not self.boss._boom and self.boss.bullet_delay == self.boss_bullet_delay_next:
                    self.boss.bullet_delay = 0
                    self.create_boss_bullet()

        # if not self.boss_created and len(self.damages) == 1:  # если вдруг случится баг и damage не исчезнет
            # for damage in self.damages:
               # self.objects.remove(damage)

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
            '''self.create_alien_UFO()
            self.create_alien_Triangle()
            self.create_alien_Bug()
            self.create_alien_Meteor()'''
            a = random.randint(1, 4)
            if a == 1:
                self.create_alien_ufo()
            if a == 2:
                self.create_alien_triangle()
            if a == 3:
                self.create_alien_bug()
            if a == 4:
                self.create_alien_meteor()

        for bullet in self.bullets:
            if intersect(self.screen, bullet.rect):
                for alien in self.aliens:
                    if intersect(alien.rect, bullet.rect):
                        self.create_boom(alien.rect.left, alien.rect.top)
                        self.objects.remove(bullet)
                        self.bullets.remove(bullet)
                        self.objects.remove(alien)
                        self.aliens.remove(alien)
                        self.score = self.score + 1
                        self.sound_effects['brick_hit'].play()
                        break
            else:
                self.objects.remove(bullet)
                self.bullets.remove(bullet)
        for boom in self.booms:
            if boom.life <= 0:
                self.booms.remove(boom)
                self.objects.remove(boom)

    def handle_boss(self):
        def intersect(s, b):
            return s.left < b.right and s.right > b.left and s.top < b.bottom and s.bottom > b.top

        if self.rocket.boomed:
            self.game_over = True
            return

        for bullet in self.bullets:
            if intersect(self.screen, bullet.rect):
                if intersect(self.boss.rect, bullet.rect):
                    if self.boss in self.objects and self.boss.hp == 1:
                        self.create_boom(self.boss.rect.left, self.boss.rect.top)
                        self.objects.remove(bullet)
                        self.bullets.remove(bullet)
                        self.objects.remove(self.boss)
                        self.score = self.score + 5
                        self.sound_effects['brick_hit'].play()
                        self.boss._boom = True
                        self.boss_score += 50
                        c.boss_hp += 10
                        self.boss_bullet_delay_next -= 8
                        self.boss_created = False

                    if self.boss in self.objects and self.boss.hp > 1:
                        if self.boss.introduction_damage:  # выезжает
                            # self.create_damage(self.boss.rect.left - 3,
                            #                  self.boss.rect.top)  # +5 чтобы урон не отставал от текстуры босса
                            self.boss._damage = True
                            self.boss.hp -= 1
                            self.objects.remove(bullet)
                            self.bullets.remove(bullet)
                            break
                        elif self.boss.switcher and not self.boss.introduction_damage and self.boss.hp > 1:  # едет вверх
                            # self.create_damage(self.boss.rect.left,
                            #                   self.boss.rect.top - 3)  # -3 чтобы урон не отставал от текстуры босса
                            self.boss._damage = True
                            self.boss.hp -= 1
                            self.objects.remove(bullet)
                            self.bullets.remove(bullet)
                            break
                        elif not self.boss.switcher and not self.boss.introduction_damage and self.boss.hp > 1:  # едет вниз
                            # self.create_damage(self.boss.rect.left,
                            #                 self.boss.rect.top + 3)  # +4 чтобы урон не отставал от текстуры босса
                            self.boss._damage = True
                            self.boss.hp -= 1
                            self.objects.remove(bullet)
                            self.bullets.remove(bullet)
                            break
            else:
                self.objects.remove(bullet)
                self.bullets.remove(bullet)

        for boss_bullet in self.boss_bullets:
            if not intersect(self.screen, boss_bullet.rect):
                self.objects.remove(boss_bullet)
                self.boss_bullets.remove(boss_bullet)
            if intersect(self.rocket.rect, boss_bullet.rect):
                self.rocket.boom()
                self.sound_effects['brick_hit'].play()
                return

        for boom in self.booms:
            if boom.life <= 0:
                self.booms.remove(boom)
                self.objects.remove(boom)

        for damage in self.damages:
            if damage.life <= 0:
                self.damages.remove(damage)
                self.objects.remove(damage)

    def leaderboard(self):
        f = open('C:\\Users\\gov99\\OneDrive\\Документы\\информатика\\18.txt', 'r')

        c = 1
        a1 = []
        s1 = []

        for line in f:
            if c == 1:
                s1.append(line)
            if c == 2:
                a1.append(int(line))
            if c == 3:
                c = 0
            c += 1

        a2 = a1.copy()
        s2 = s1.copy()

        s = input('Enter your nickname: ')
        a = self.score

        if s2.count(s + '\n') >= 1 and a > a2[s2.index(s + '\n')]:
            a2.remove(a2[s2.index(s + '\n')])
            a1.remove(a1[s2.index(s + '\n')])
            s2.remove(s + '\n')
        s2.append(s + '\n')
        a2.append(a)
        a1.append(a)

        a2.sort()

        f = open('C:\\Users\\gov99\\OneDrive\\Документы\\информатика\\18.txt', 'w')
        for i in range(0, len(a2)):
            f.write(s2[a1.index(a2[i])])
            f.write(str(a2[i]))
            f.write('\n')
            f.write('\n')
        f.close()

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
