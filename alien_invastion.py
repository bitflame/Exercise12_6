import sys

import pygame

from settings import Settings
from ship import Ship
from bullet import Bullet
from droplet import Droplet

class AlienInvasion: 
    """Overall class to manage game """
    def __init__(self):
        """initialize the game"""
        pygame.init()
        self.clock = pygame.time.Clock()
        self.settings = Settings()
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        self.screen = pygame.display.set_mode((1200,800))
        # self.screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
        # self.settings.screen_width = self.screen.get_rect().width
        # self.settings.screen_height = self.screen.get_rect().height
        pygame.display.set_caption("Alien Invasion")
        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.droplets = pygame.sprite.Group()
        # set background color 
        self.bg_color = (230, 230, 230)
        
    def run_game(self):
        """Start the main loop fo the game"""
        while True:
            self._check_events()
            self.ship.update()
            self._update_bullets()
            self._update_droplets()
            self._update_screen()
            self.clock.tick(60)
    
    def _check_events(self):
        """Respond to keypresses and mouse events"""
        # Watch for keboard and mouse envents.
        for event in pygame.event.get(): #<- this is called event loop
            # if event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
                
    def _fire_bullet(self):
        """Crete a new bullet and add it to the bullets group."""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)
                
    def _update_bullets(self):
        """Update postion of bullets adn get rigd fo old bullets"""
        #update bullet position
        self.bullets.update()
            # Get rigt of bullets that have disappeared.
        for bullet in self.bullets.copy():
            if bullet.rect.right >= self.screen.get_rect().right:
                self.bullets.remove(bullet)         
        # print(len(self.bullets)) <- This is to make sure bullets are deleted.
    def _update_droplets(self):
        self.droplets.update()
        for droplet in self.droplets.copy():
            if droplet.rect.bottom > self.screen.get_rect().bottom:
                self.droplets.remove(droplet)
        droplet = Droplet(self)
        droplet_width = droplet.rect.width
        droplet_height = droplet.rect.height
        current_x = droplet_width
        while current_x < (self.settings.screen_width -2 * droplet_width):
            new_droplet = Droplet(self)
            new_droplet.x = current_x
            new_droplet.rect.x = current_x
            self.droplets.add(new_droplet)
            current_x += 2 * droplet_width     
    def _update_screen(self):
        # Redraw the screen during each pass through the loop.
            self.screen.fill(self.settings.bg_color)
            for bullet in self.bullets.sprites():
                bullet.draw_bullet()
            self.droplets.draw(self.screen)
            self.ship.blitme()     
            # Make the most recently drawn screen visible.
            pygame.display.flip()
    def _check_keydown_events(self, event):
        """Respond to keypresses."""
        if event.key == pygame.K_UP:
            self.ship.moving_up = True
        elif event.key == pygame.K_DOWN:
            self.ship.moving_down = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
                self._fire_bullet()
        
    def _check_keyup_events(self, event):
        """Respond to key releases."""
        if event.key == pygame.K_UP:
            self.ship.moving_up = False
        elif event.key == pygame.K_DOWN:
            self.ship.moving_down = False
            
if __name__ == '__main__': #<-Only run if the file is called directly 
    # Make a game instance, and run the game.
    ai = AlienInvasion()
    ai.run_game()
    print("Hello")
    