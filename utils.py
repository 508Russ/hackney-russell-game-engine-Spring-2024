# this 'cooldown' class is designed to help us control time
import pygame as pg

from math import floor

class Timer():
    def __init__(self, game):
        # Initialize the Timer with a reference to the game instance
        self.game = game
        # Initialize the current time and event time
        self.current_time = 0
        self.event_time = 0
        # Initialize the countdown value
        self.cd = 0
        # Set the interval for mob spawning (in seconds)
        self.spawn_interval = 10
        # Store the time when the last mob was spawned
        self.last_spawn_time = 0

    # Update the timer
    def ticking(self):
        # Update current time (in seconds) using pygame's time function
        self.current_time = floor((pg.time.get_ticks()) / 1000)
        # If there is an active cooldown, update the countdown
        if self.cd > 0:
            self.countdown()
        
    # Update the countdown
    def countdown(self):
        if self.cd > 0:
            # Decrease the countdown by the delta time since the last frame
            self.cd -= self.game.dt

    # Reset the event time to the current time
    def event_reset(self):
        self.event_time = floor((pg.time.get_ticks()) / 1000)

    # Get the current value of the countdown timer
    def get_countdown(self):
        return floor(self.cd)

    # Update the current time
    def get_current_time(self):
        self.current_time = floor((pg.time.get_ticks()) / 1000)

    # Check if enough time has passed to spawn a new mob
    def should_spawn_mob(self):
        if self.current_time - self.last_spawn_time >= self.spawn_interval:
            # Update the last spawn time to the current time
            self.last_spawn_time = self.current_time
            return True
        return False
