import pygame
from pygame.sprite import Sprite

class Droplet(Sprite):
    """A class to represent rain"""
    def __init__(self, ai_game):
        super().__init__()
        self.screen = ai_game.screen
    
        #load the rain image and set its rect attributes
        self.image = pygame.image.load('images/side0001.png')
        self.rect = self.image.get_rect()
        # start each new rain drop near the top left of the screen
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height
        #store the rain drop's exact horizontal position
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)
        self.settings = ai_game.settings
        
    def update(self):
         self.y += self.settings.drop_speed
         self.rect.y = self.y
         
    def check_height(self):
        screen_rect = self.screen.get_rect()
        return self.rect.bottom > screen_rect.bottom