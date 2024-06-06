import pygame.font
class Button:
    def __init__(self, aigame, msg):
        """initialize button attributes"""
        self.screen = aigame.screen
        self.screen_rect = self.screen.get_rect()
        # Set dimenstions and attributes
        self.width, self.hight = 200, 50
        self.button_color = (0, 135, 0)
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 48)
        # build the button's rect object
        self.rect = pygame.Rect(0, 0, self.width, self.hight)
        self.rect.center = self.screen_rect.center
        # the button message needs to be preped 
        self._prep_message(msg)
        
    def _prep_message(self, msg):
        self.msg_image = self.font.render(msg, True, self.text_color, self.button_color)    
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center
        
    def draw_button(self):
        """Draw blank and then draw a message"""
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)