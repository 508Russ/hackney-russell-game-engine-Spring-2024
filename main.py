# This file was created by: Russell Hackney


# creat mob that chases you, add timer that goes up, create start screen
'''
Game design truths:
goals, rules, feedback, freedom, what the verb, and will it form a sentence 

'''
import pygame as pg
from settings import *
from sprites import *
from utils import *
from random import randint
import sys
from os import path

# added this math function to round down the clock
from math import floor



# Define game class...
class Game:
    # Define a special method to init the properties of said class...
    def __init__(self):
        # init pygame
        pg.init()
        # set size of screen and be the screen
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        # setting game clock 
        self.clock = pg.time.Clock()
        self.load_data()
        # added images folder and image in the load_data method for use with the player
    def load_data(self):
        game_folder = path.dirname(__file__)
        pictures = path.join(game_folder, 'picture')
        self.player_img = pg.image.load(path.join(pictures, 'spongebob.png')).convert_alpha()
        self.map_data = []
        '''
        The with statement is a context manager in Python. 
        It is used to ensure that a resource is properly closed or released 
        after it is used. This can help to prevent errors and leaks.
        '''
        with open(path.join(game_folder, 'map.txt'), 'rt') as f:
            for line in f:
                print(line)
                self.map_data.append(line)

    # Create run method which runs the whole GAME
    def new(self):
        # create timer
        self.cooldown = Timer(self)
        print("create new game...")
        self.all_sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.coins = pg.sprite.Group()
        self.mobs = pg.sprite.Group()
        self.power_ups = pg.sprite.Group()
        # self.player1 = Player(self, 1, 1)
        # for x in range(10, 20):
        #     Wall(self, x, 5)
        for row, tiles in enumerate(self.map_data):
            print(row)
            for col, tile in enumerate(tiles):
                print(col)
                if tile == '1':
                    print("a wall at", row, col)
                    Wall(self, col, row)
                if tile == 'P':
                    self.player = Player(self, col, row)
                if tile == 'C':
                    Coin(self, col, row)
                if tile == 'M':
                    Mob(self, col, row)
                if tile == 'U':
                    PowerUp(self, col, row)

    def run(self):
        # 
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            self.update()
            self.draw()
    def quit(self):
         pg.quit()
         sys.exit()

    def update(self):
        # tick the test timer
        self.cooldown.ticking()
        self.all_sprites.update()
    
    def draw_grid(self):
         for x in range(0, WIDTH, TILESIZE):
              pg.draw.line(self.screen, LIGHTGREY, (x, 0), (x, HEIGHT))
         for y in range(0, HEIGHT, TILESIZE):
              pg.draw.line(self.screen, LIGHTGREY, (0, y), (WIDTH, y))
    
    def draw_text(self, surface, text, size, color, x, y):
        font_name = pg.font.match_font('arial')
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.topleft = (x,y)
        surface.blit(text_surface, text_rect)
    
    def draw(self):
            self.screen.fill(BGCOLOR)
            # self.draw_grid()
            self.all_sprites.draw(self.screen)
            # draw the timer
            self.draw_text(self.screen, str(self.cooldown.current_time), 24, WHITE, WIDTH/2 - 32, 2)
            self.draw_text(self.screen, str(self.cooldown.event_time), 24, WHITE, WIDTH/2 - 32, 80)
            self.draw_text(self.screen, str(self.cooldown.get_countdown()), 24, WHITE, WIDTH/2 - 32, 120)
            pg.display.flip()

    def events(self):
         for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            # if event.type == pg.KEYDOWN:
            #     if event.key == pg.K_LEFT:
            #         self.player.move(dx=-1)
            #     if event.key == pg.K_RIGHT:
            #         self.player.move(dx=1)
            #     if event.key == pg.K_UP:
            #         self.player.move(dy=-1)
            #     if event.key == pg.K_DOWN:
            #         self.player.move(dy=1)
    # Define a method to show the start screen
def show_start_screen(self):
    # Fill the screen with the background color
    self.screen.fill(BGCOLOR)
    # Draw text on the screen to prompt the user to press any key to start
    self.draw_text(self.screen, "Press any key to start", 50, PURPLE, WIDTH/2-180, HEIGHT/2-50)
    # Update the display
    pg.display.flip()
    # Wait for the user to press a key
    self.wait_for_key()

# Define a method to wait for a key press
def wait_for_key(self):
    # Set the flag to True to indicate waiting for a key press
    waiting = True
    # Continue waiting until a key is pressed
    while waiting:
        # Control the frame rate
        self.clock.tick(FPS)
        # Check for events (e.g., key press or window close)
        for event in pg.event.get():
            # If the user closes the window, exit the game
            if event.type == pg.QUIT:
                waiting = False
                self.quit()
            # If the user releases a key, stop waiting
            if event.type == pg.KEYUP:
                waiting = False

    
# Instantiate the game... 
g = Game()
# use game method run to run
g.show_start_screen()
while True:
    g.new()
    g.run()
    # g.show_go_screen()