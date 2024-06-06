import pygame
from pygame.sprite import Sprite

class Ship(Sprite): 
    def __init__(self, ai_game):
        """initialize the ship and set its sarting position"""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = ai_game.screen.get_rect()
        # Load the ship images and get its rect.
        self.image = pygame.image.load('images/rocket_sideways.png')
        self.rect = self.image.get_rect()
        # start each new ship at the bottom center of teh screen.
        self.rect.midleft = self.screen_rect.midleft
        # store a float for the ship's exact horizontal position
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)
        # self.moving_right = False
        # self.moving_left = False
        self.moving_down = False
        self.moving_up = False
        
    def update(self):
        """Update ship's position based on movement flags"""
        # Update the ship's x value, not the rect
        if self.moving_down and self.rect.bottom < self.screen_rect.bottom:
            self.y += self.settings.ship_speed
        if self.moving_up and self.rect.top > 0: 
            self.y -= self.settings.ship_speed
        #Update rectangle objects
        self.rect.y = self.y
        
    def blitme(self):
        """Draw the ship at its current location"""
        self.screen.blit(self.image, self.rect)
    
    def center_ship(self):
        """Center the ship on the screen"""
        self.rect.midleft = self.screen_rect.midleft
        self.y = float(self.rect.y)
    