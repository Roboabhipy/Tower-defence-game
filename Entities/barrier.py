import pygame

import Data.constants as constants

from Utils.UtilityFunction import load_image


class Barrier():
    def __init__(self, x, y, image, health):
        print("created barrier")
        self.rect = pygame.Rect(
            x, y, constants.GRID_WIDTH, constants.GRID_HEIGHT)
        self.health = health
        self.image = load_image(
            (f"Blocks/{image}"), self.rect.width, self.rect.height, 0)

    def hit(self, attack_dmg):
        self.health -= attack_dmg

    def draw(self):
        constants.WIN.blit(self.image, (self.rect.x, self.rect.y))
