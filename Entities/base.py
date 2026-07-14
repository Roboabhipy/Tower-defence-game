import pygame
import Data.constants as constants
from Components.health import Health


class Base():
    def __init__(self, x, y, width, height, colour, health):
        self.rect = pygame.Rect(x, y, width, height)
        self.x, self.y = self.rect.center
        self.colour = colour
        self.health = health
        self.health_rect = Health(
            self.rect.centerx - 37, self.rect.y - 15, 75, 5, health, health)
        self.neighbours = []

    def hit(self, attack):
        self.health -= attack
        self.health_rect.update_health(self.health)

    def draw(self):
        pygame.draw.rect(constants.WIN, self.colour, self.rect)
        pygame.draw.rect(constants.WIN, "red", self.health_rect)
