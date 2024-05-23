class Settings:
    """A class to store all the settings"""
    def __init__(self):
        """Initialize the game's settings"""
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230)
        self.ship_speed = 1.5
        self.ship_limit = 3
        # bullet settings
        self.bullet_speed = 2.0
        self.bullet_width = 15
        self.bullet_height = 3
        self.bullet_color = (60, 60, 60)
        self.bullets_allowed = 3
        # Alien settings
        self.alien_speed = 1.0
        # actually it is more of approach speed since this version's aliens move to left
        self.fleet_drop_speed = 10
        self.fleet_direction = 1
        