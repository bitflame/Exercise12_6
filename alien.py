import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    """A class to reqeust a single alien"""
    def __init__(self, ai_game):
        """Initialize the alien and set its starting position"""
        super().__init__()
        self.screen = ai_game.screen
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