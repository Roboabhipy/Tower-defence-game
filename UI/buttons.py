import pygame
import Data.constants as constants


class Buttons():
    def __init__(self, text, function, button_col, text_col, center, price, padding=10):
        self.selected_block = function
        self.text = text
        self.original_button_colour = button_col
        self.text_colour = text_col
        self.colour = self.original_button_colour
        self.price = price

        self.text_surface = constants.FONT.render(self.text, True, text_col)
        self.width = max(100, self.text_surface.get_width() + padding)
        self.height = max(50, self.text_surface.get_height() + padding)
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = center

    def mouse_detection(self, mouse_pos, coins):
        self.colour = self.original_button_colour
        if not self.rect.collidepoint(mouse_pos):
            return

        if coins >= self.price:
            self.colour = "green"
        else:
            self.colour = "red"

    def get_function(self):
        return self.selected_block

    def draw(self):
        pygame.draw.rect(constants.WIN, self.colour, self.rect)
        pygame.draw.rect(constants.WIN, "black", self.rect, 3)
        constants.WIN.blit(self.text_surface, (self.rect.centerx -
                           self.text_surface.get_width()/2, self.rect.centery))
