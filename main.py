import pygame as pg
from settings import *
from sprites import *
from utils import *
from random import randint
import sys
from os import path
from math import floor

# Game class to encapsulate the game functionalities
class Game:
    def __init__(self):
        pg.init()
        # Initialize screen with width and height
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        # Set window title
        pg.display.set_caption(TITLE)
        # Initialize clock to manage frame rate
        self.clock = pg.time.Clock()
        # Load game data such as images and map
        self.load_data()

    def load_data(self):
        # Get the directory of the current script
        game_folder = path.dirname(__file__)
        # Define the path to the pictures directory
        pictures = path.join(game_folder, 'picture')
        # Load player and coin images
        self.player_img = pg.image.load(path.join(pictures, 'spongebob.png')).convert_alpha()
        self.coin_img = pg.image.load(path.join(pictures, 'coin.png')).convert_alpha()
        # Load map data from text file
        self.map_data = []
        with open(path.join(game_folder, 'map.txt'), 'rt') as f:
            for line in f:
                self.map_data.append(line)

    def new(self):
        # Initialize the Timer object for cooldown management
        self.cooldown = Timer(self)
        # Create sprite groups
        self.all_sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.coins = pg.sprite.Group()
        self.mobs = pg.sprite.Group()
        self.power_ups = pg.sprite.Group()
        # Parse the map data to create game objects
        for row, tiles in enumerate(self.map_data):
            for col, tile in enumerate(tiles):
                if tile == '1':
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
        # Main game loop
        self.playing = True
        while self.playing:
            # Control the frame rate
            self.dt = self.clock.tick(FPS) / 1000
            # Handle events
            self.events()
            # Update game state
            self.update()
            # Draw the game
            self.draw()

    def quit(self):
        # Quit pygame and exit the program
        pg.quit()
        sys.exit()

    def update(self):
        # Update the cooldown timer
        self.cooldown.ticking()
        # Check if a new mob should spawn
        if self.cooldown.should_spawn_mob():
            self.spawn_mob()
        # Update all sprites
        self.all_sprites.update()

    def draw(self):
        # Fill the screen with background color
        self.screen.fill(BGCOLOR)
        # Draw all sprites on the screen
        self.all_sprites.draw(self.screen)
        # Draw the cooldown timer and other debug info
        self.draw_text(self.screen, str(self.cooldown.current_time), 24, WHITE, WIDTH/2 - 32, 2)
        self.draw_text(self.screen, str(self.cooldown.event_time), 24, WHITE, WIDTH/2 - 32, 80)
        self.draw_text(self.screen, str(self.cooldown.get_countdown()), 24, WHITE, WIDTH/2 - 32, 120)
        # Update the display
        pg.display.flip()

    def events(self):
        # Handle events such as quitting the game
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_t:
                    self.player.teleport_to_cursor()

    def show_start_screen(self):
        # Display the start screen
        self.screen.fill(BGCOLOR)
        self.draw_text(self.screen, "Press any key to start", 50, PURPLE, WIDTH/2-180, HEIGHT/2-50)
        pg.display.flip()
        # Wait for a key press to start the game
        self.wait_for_key()

    def wait_for_key(self):
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.quit()
                if event.type == pg.KEYUP:
                    waiting = False

    def spawn_mob(self):
        # Generate random coordinates within the grid
        x = randint(0, WIDTH // TILESIZE - 1)
        y = randint(0, HEIGHT // TILESIZE - 1)
        # Create a new mob at the generated coordinates
        Mob(self, x, y)

    def draw_text(self, surface, text, size, color, x, y):
        # Draw text on the screen
        font_name = pg.font.match_font('arial')
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.topleft = (x, y)
        surface.blit(text_surface, text_rect)

# Instantiate and run the game
g = Game()
g.show_start_screen()
while True:
    g.new()
    g.run()
