import pygame
import Data.constants as constants


class Health():
    def __init__(self, x, y, width, height, crnt_health, max_health):
        self.rect = pygame.Rect(x, y, (crnt_health/max_health)*width, height)
        self.width = width
        self.max_health = max_health

    def update_health(self, health):
        self.rect.width = (health/self.max_health)*self.width

    def move(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy
