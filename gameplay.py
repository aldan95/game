import random

class Gameplay:

    def __init__(self, breakout):
        self.breakout = breakout
        self.gametick = 0
        self.second = 0
        self.required_alien_count = 2

    def tick(self, alien_count):
        self.gametick += 1
        self.second = self.gametick / 30
        if alien_count < self.required_alien_count:
            a = random.randint(1,4)
            if a == 1:
                self.breakout.create_alien_UFO()
            if a == 2:
                self.breakout.create_alien_Triangle()
            if a == 3:
                self.breakout.create_alien_Bug()
            if a == 4:
                self.breakout.create_alien_Meteor()

