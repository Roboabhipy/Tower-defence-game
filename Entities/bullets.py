import pygame
import math
import Utils.UtilityFunction as UtilityFunction
import Data.constants as constants


class Bullets():
    def __init__(self, x, y, width, height, angle, vel, colour):
        self.rect = pygame.Rect(x, y, width, height)
        self.angle = angle
        self.vel = vel
        self.colour = colour
        rad = math.radians(angle)
        self.dx = math.cos(rad) * self.vel
        self.dy = math.sin(rad) * self.vel

    def movement(self):
        self.rect.x += self.dx
        self.rect.y += self.dy

    def draw(self):
        points = UtilityFunction.polygon_points(
            self.rect.x, self.rect.y, self.rect.height, self.rect.width, self.angle)
        pygame.draw.polygon(constants.WIN, self.colour, points)
