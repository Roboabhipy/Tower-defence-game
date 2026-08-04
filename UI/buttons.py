import pygame
import Data.constants as constants


class Buttons():
    hovering = False

    def __init__(self, text, function, button_col, text_col, center, price=None, padding=10, width=100, height=50):
        self.selected_block = function
        self.text = text
        self.original_button_colour = button_col
        self.text_colour = text_col
        self.colour = self.original_button_colour
        self.price = price

        self.text_surface = constants.FONT.render(self.text, True, text_col)
        self.width = max(width, self.text_surface.get_width() + padding)
        self.height = max(height, self.text_surface.get_height() + padding)
        
        if self.price != None:
            self.price_surface = constants.FONT.render(
            str(self.price), True, self.colour)

        self.base_rect = pygame.Rect(0, 0, self.width, self.height)
        self.base_rect.center = center

        self.scale = 1
        self.target_scale = 1
        self.animation_speed = 0.1

    def mouse_detection(self, mouse_pos, coins):
        self.colour = self.original_button_colour
        self.scale += (self.target_scale - self.scale)*self.animation_speed
        
        if not self.base_rect.collidepoint(mouse_pos):
            self.target_scale = 1
            return

        Buttons.hovering = True
        self.target_scale = 1.1
        if self.price != None:
            if coins >= self.price:
                self.colour = "green"
            else:
                self.colour = "red"

    def get_function(self):
        return self.selected_block

    @staticmethod
    def hover():
        if Buttons.hovering:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

        Buttons.hovering = False

    def draw(self):
        scaled_rect = pygame.Rect(self.base_rect.x, self.base_rect.y,
                                  self.base_rect.width*self.scale, self.base_rect.height*self.scale)
        scaled_rect.center = self.base_rect.center
        pygame.draw.rect(constants.WIN, self.colour, scaled_rect)
        pygame.draw.rect(constants.WIN, "white", scaled_rect, 3)
        constants.WIN.blit(self.text_surface, (self.base_rect.centerx -
                           self.text_surface.get_width()/2, self.base_rect.centery - self.text_surface.get_height() / 2))

        if self.target_scale != 1 and self.price != None:
            constants.WIN.blit(self.price_surface, (self.base_rect.centerx -
                                                    self.text_surface.get_width()/2, scaled_rect.bottom + 10))
