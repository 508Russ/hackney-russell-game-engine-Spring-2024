import pygame as pg
from settings import *

class MainMenu:
    def __init__(self):
        self.font = pg.font.Font(None, 36)
        self.menu_items = ["Start Game", "Quit"]
        self.selected_item = 0
    
    def draw(self, screen):
        screen.fill(BGCOLOR)
        for i, item in enumerate(self.menu_items):
            color = WHITE if i == self.selected_item else LIGHTGREY
            text = self.font.render(item, True, color)
            text_rect = text.get_rect(center=(WIDTH / 2, HEIGHT / 2 + i * 40))
            screen.blit(text, text_rect)
    
    def handle_event(self, event):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_UP:
                self.selected_item = (self.selected_item - 1) % len(self.menu_items)
            elif event.key == pg.K_DOWN:
                self.selected_item = (self.selected_item + 1) % len(self.menu_items)
            elif event.key == pg.K_RETURN:
                if self.selected_item == 0:
                    return "start"
                elif self.selected_item == 1:
                    return "quit"
        return None
