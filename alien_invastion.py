import sys

import pygame

from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien

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
        self.aliens = pygame.sprite.Group()
        self._create_fleet()
        # set background color 
        self.bg_color = (230, 230, 230)
        
    def _create_fleet(self):
        """Create the fleet of aliens"""
        # Crete an alien and keep adding aliens until there's no room 
        # Spacing between aliens is one alien width
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        current_x = self.settings.screen_width -3 * alien_width
        current_y = alien_height 
        while current_x > (3 * alien_width):
            while current_y < (self.settings.screen_height - 2 * alien_height):
                self._create_alien(current_x, current_y)
                current_y += 2 * alien_height
            # Finish a column, reset y value, and decrement x
            current_y = alien_height
            current_x -= 2 * alien_width
            
    def _create_alien(self, x_position, y_position):
        """Create an alien and place it in the row"""
        new_alien = Alien(self)
        new_alien.y = y_position
        new_alien.rect.y = y_position
        new_alien.rect.x = x_position
        self.aliens.add(new_alien)   
        
    def _check_fleet_edges(self):
        """Respond appropriately if any aliens have reached an edge"""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break
            
    def _change_fleet_direction(self):
        """Move the entire fleet closer to rocket on the left side of the screen"""
        for alien in self.aliens.sprites():
            alien.rect.x -= self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1
                 
    def run_game(self):
        """Start the main loop fo the game"""
        while True:
            self._check_events()
            self.ship.update()
            self._update_bullets()
            self._update_aliens()
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
        # Check for any bullets that have hit the aliens.
        # If so, get rid of the bullet and alien
                
    def _update_aliens(self):
        """Update the positions of all alisens in the fleet"""
        self._check_fleet_edges()
        self.aliens.update()
        
    def _update_bullets(self):
        """Update postion of bullets adn get rigd fo old bullets"""
        #update bullet position
        self.bullets.update()
            # Get rigt of bullets that have disappeared.
        for bullet in self.bullets.copy():
            if bullet.rect.right >= self.screen.get_rect().right:
                self.bullets.remove(bullet)         
        # print(len(self.bullets)) <- This is to make sure bullets are deleted.
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)
        if not self.aliens:
            # Destroy existing bullets and create new fleet
            self.bullets.empty()
            self._create_fleet()
            
    def _update_screen(self):
        # Redraw the screen during each pass through the loop.
            self.screen.fill(self.settings.bg_color)
            for bullet in self.bullets.sprites():
                bullet.draw_bullet()
            self.ship.blitme()   
            self.aliens.draw(self.screen)  
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
    