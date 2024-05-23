import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    """A class to reqeust a single alien"""
    def __init__(self, ai_game):
        """Initialize the alien and set its starting position"""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        screen_rect = self.screen.get_rect()
        #Load the alien image and set its rect attribute
        self.image = pygame.image.load('images/alien.bmp')
        self.rect = self.image.get_rect()
        
        # Start each new alien near the top right of the screen
        # self.rect.x = self.rect.width
        self.rect.x =  screen_rect.right - (self.rect.width * 2)
        self.rect.y = self.rect.height
        
        # store the alien's exact horizonatl position
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)
        
    def update(self):
        """Move the alien down"""
        self.y += self.settings.alien_speed * self.settings.fleet_direction
        self.rect.y = self.y
    
    def check_edges(self):
        screen_rect = self.screen.get_rect()
        return (self.rect.top < 0) or (self.rect.bottom > screen_rect.bottom )
    