# this 'cooldown' class is designed to help us control time
import pygame as pg

from math import floor

class Timer():
    def __init__(self, game):
        self.game = game
        self.current_time = 0
        self.event_time = 0
        self.cd = 0
        self.spawn_interval = 10  # Interval for mob spawn
        self.last_spawn_time = 0  # Time when the last mob was spawned

    def ticking(self):
        self.current_time = floor((pg.time.get_ticks())/1000)
        if self.cd > 0:
            self.countdown()
        
    def countdown(self):
        if self.cd > 0:
            self.cd = self.cd - self.game.dt

    def event_reset(self):
        self.event_time = floor((pg.time.get_ticks())/1000)

    def get_countdown(self):
        return floor(self.cd)

    def get_current_time(self):
        self.current_time = floor((pg.time.get_ticks())/1000)

    def should_spawn_mob(self):
        if self.current_time - self.last_spawn_time >= self.spawn_interval:
            self.last_spawn_time = self.current_time
            return True
        return False
