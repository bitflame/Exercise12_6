import sys
from time import sleep

import pygame

from settings import Settings
from ship import Ship
from game_stats import GameStats
from bullet import Bullet
from alien import Alien
from button import Button
from scoreboard import ScoreBoard

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
        pygame.display.set_caption("Sideways Shooter")
        # Create an instance to store game stats and create a scoreboard
        self.stats = GameStats(self)
        self.sb = ScoreBoard(self)
        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self._create_fleet()
        # set background color 
        self.bg_color = (230, 230, 230)
        self.game_active = False
        # Make the play button
        self.play_button = Button(self, "Play") 
        
    def _ship_hit(self):
        """Respond to the ship being hit by an alien."""
        if self.stats.ships_left > 0:
            # decrement ships_left
            self.stats.ships_left -= 1
            # Get rid of any remaining bullets and aliens
            self.bullets.empty()
            self.aliens.empty()
            # Create a new fleet and center the ship 
            self._create_fleet()
            self.ship.center_ship()
            # Pause
            sleep(0.5)  
        else: 
            self.game_active = False  
            pygame.mouse.set_visible(True)
        
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
            if self.game_active:
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
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)
            
    def _check_play_button(self, mouse_pos):
        """Start a new game when the player clicks play."""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.game_active:
            self.stats.reset_stats()
            self.game_active = True
            # Get rid of any remaining bullets and aliens. 
            self.bullets.empty()
            self.aliens.empty()
            # Create a new fleet and center the ship.
            self._create_fleet()
            self.ship.center_ship()
            # Hide the mouse cursor
            pygame.mouse.set_visible(False)
            # Reset the game settings.
            self.settings.initialize_dynamic_settings()
            
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
        # Look for alien-ship collisions
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()
        # Look for aliens hitting the left wall
        self._check_aliens_bottom()
        
    def _check_aliens_bottom(self):
        """This is actually the left wall not the bottom"""
        for alien   in self.aliens.sprites():
            if alien.rect.left <= 0:
                # Treat this the same as if the ship got hit. 
                self._ship_hit()
                break
            
    def _update_bullets(self):
        """Update postion of bullets adn get rigd fo old bullets"""
        #update bullet position
        self.bullets.update()
            # Get rigt of bullets that have disappeared.
        for bullet in self.bullets.copy():
            if bullet.rect.right >= self.screen.get_rect().right:
                self.bullets.remove(bullet)         
        # print(len(self.bullets)) <- This is to make sure bullets are deleted.
        self._check_bullet_alien_collisions()
            
    def _check_bullet_alien_collisions(self):
        """Respond to bullet-alien collisions."""
        # Remove any bullets and alients that have collided.
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)
        if collisions:
            self.stats.score += self.settings.alien_points
            self.sb.prep_score()
        if not self.aliens:
            # Destroy existing bullets and create new fleet
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()
            
    def _update_screen(self):
        # Redraw the screen during each pass through the loop.
            self.screen.fill(self.settings.bg_color)
            for bullet in self.bullets.sprites():
                bullet.draw_bullet()
            self.ship.blitme()   
            self.aliens.draw(self.screen)  
            self.sb.show_score()
            # Draw the play button if the game is inactive
            if not self.game_active:
                self.play_button.draw_button()
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
    