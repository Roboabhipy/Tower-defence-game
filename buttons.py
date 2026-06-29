import pygame
import constants


class Buttons():
    def __init__(self, x, y, width, height, function, text, colour):
        self.rect = pygame.Rect(x, y, width, height)
        self.selected_block = function
        self.text = text
        self.original_colour = colour
        self.colour = colour

    def mouse_detection(self, mouse_pos):
        self.colour = self.original_colour
        if self.rect.collidepoint(mouse_pos):
            self.colour = (255, 255, 255, 128)

    def get_function(self):
        return self.selected_block

    def draw(self):
        pygame.draw.rect(constants.WIN, self.colour, self.rect)
        pygame.draw.rect(constants.WIN, "black", self.rect, 3)
        text_surface = constants.FONT.render(self.text, True, "black")
        constants.WIN.blit(text_surface, (self.rect.centerx -
                           text_surface.get_width()/2, self.rect.centery))
