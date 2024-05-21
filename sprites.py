import pygame as pg
from settings import *
from utils import *
from random import choice

# Player class definition
class Player(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        # Initialize sprite groups and call the parent class (Sprite) initializer
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        
        # Set up the game reference and load the player image
        self.game = game
        self.image = game.player_img
        self.rect = self.image.get_rect()
        
        # Initialize velocity (vx, vy), position (x, y), and player attributes
        self.vx, self.vy = 0, 0
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.rect.x = self.x
        self.rect.y = self.y
        self.moneybag = 0
        self.speed = 300  # Player movement speed
        self.status = ""
        self.hitpoints = 100
        self.cooling = False

    # Method to handle player movement based on key inputs
    def get_keys(self):
        # Reset velocities
        self.vx, self.vy = 0, 0
        
        # Get the current key states
        keys = pg.key.get_pressed()
        
        # Update velocities based on key inputs
        if keys[pg.K_LEFT] or keys[pg.K_a]:
            self.vx = -self.speed
        if keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.vx = self.speed
        if keys[pg.K_UP] or keys[pg.K_w]:
            self.vy = -self.speed
        if keys[pg.K_DOWN] or keys[pg.K_s]:
            self.vy = self.speed
        
        # Adjust speed for diagonal movement to keep it consistent
        if self.vx != 0 and self.vy != 0:
            self.vx *= 0.7071
            self.vy *= 0.7071

    # Method to handle collision with walls
    def collide_with_walls(self, dir):
        if dir == 'x':
            # Check for collisions in the x direction
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                if self.vx > 0:  # Moving right; hit the left side of the wall
                    self.x = hits[0].rect.left - self.rect.width
                if self.vx < 0:  # Moving left; hit the right side of the wall
                    self.x = hits[0].rect.right
                self.vx = 0
                self.rect.x = self.x
        if dir == 'y':
            # Check for collisions in the y direction
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                if self.vy > 0:  # Moving down; hit the top side of the wall
                    self.y = hits[0].rect.top - self.rect.height
                if self.vy < 0:  # Moving up; hit the bottom side of the wall
                    self.y = hits[0].rect.bottom
                self.vy = 0
                self.rect.y = self.y

    # Method to handle collision with various groups
    def collide_with_group(self, group, kill):
        # Check for collisions with the specified group
        hits = pg.sprite.spritecollide(self, group, kill)
        if hits:
            # Handle collision with coins
            if str(hits[0].__class__.__name__) == "Coin":
                self.moneybag += 1
            # Handle collision with power-ups
            if str(hits[0].__class__.__name__) == "PowerUp":
                effect = choice(POWER_UP_EFFECTS)
                self.game.cooldown.cd = 5
                self.cooling = True
                if effect == "Invincible":
                    self.status = "Invincible"
            # Handle collision with mobs (enemies)
            if str(hits[0].__class__.__name__) == "Mob":
                # Placeholder for mob collision logic
                pg.quit()

    # Method to teleport player to the cursor position
    def teleport_to_cursor(self):
        # Get the current mouse position
        mouse_x, mouse_y = pg.mouse.get_pos()
        
        # Update player position to the mouse position
        self.x = mouse_x
        self.y = mouse_y
        
        # Update the rectangle position to match the new coordinates
        self.rect.x = self.x
        self.rect.y = self.y

    # Update method called every frame
    def update(self):
        # Handle cooling down status
        if self.status == "Invincible":
            self.cooling = False
            self.status = ""
        
        # Update player movement based on key inputs and handle collisions
        self.get_keys()
        self.x += self.vx * self.game.dt
        self.y += self.vy * self.game.dt
        self.rect.x = self.x
        self.collide_with_walls('x')
        self.rect.y = self.y
        self.collide_with_walls('y')
        
        # Handle collisions with coins, power-ups, and mobs
        self.collide_with_group(self.game.coins, True)
        self.collide_with_group(self.game.power_ups, True)
        self.collide_with_group(self.game.mobs, False)

# Wall class definition
class Wall(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        # Initialize sprite groups and call the parent class (Sprite) initializer
        self.groups = game.all_sprites, game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        
        # Set up the game reference and create a rectangle for the wall
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

# Coin class definition
class Coin(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        # Initialize sprite groups and call the parent class (Sprite) initializer
        self.groups = game.all_sprites, game.coins
        pg.sprite.Sprite.__init__(self, self.groups)
        
        # Set up the game reference and load the coin image
        self.game = game
        self.image = game.coin_img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

# Mob (enemy) class definition
class Mob(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        # Initialize sprite groups and call the parent class (Sprite) initializer
        self.groups = game.all_sprites, game.mobs
        pg.sprite.Sprite.__init__(self, self.groups)
        
        # Set up the game reference and create a rectangle for the mob
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

    # Update method called every frame
    def update(self):
        # Placeholder for mob behavior
        pass

# PowerUp class definition
class PowerUp(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        # Initialize sprite groups and call the parent class (Sprite) initializer
        self.groups = game.all_sprites, game.power_ups
        pg.sprite.Sprite.__init__(self, self.groups)
        
        # Set up the game reference and create a rectangle for the power-up
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

    # Update method called every frame
    def update(self):
        # Placeholder for power-up behavior
        pass
