import pygame
import constants


class Blocks():
    def __init__(self, x, y, width, height, colour):
        self.rect = pygame.Rect(x, y, width, height)
        self.colour = colour

    def draw(self):
        pygame.draw.rect(constants.WIN, self.colour, self.rect)
