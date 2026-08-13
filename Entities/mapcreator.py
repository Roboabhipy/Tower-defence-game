import Data.constants as constants
from Utils.UtilityFunction import load_image
import pygame
import os
import random

tile_images = {}

for image in os.listdir("Assets/Tiles"):
    name_without_ext, ext = os.path.splitext(image)
    tile_images[name_without_ext] = load_image(
        f"Tiles\{name_without_ext}", constants.GRID_WIDTH, constants.GRID_HEIGHT, 0)


class Map():
    def __init__(self, col, row, colour, type="Obstacle"):
        self.row = row
        self.col = col
        self.x = col * constants.GRID_WIDTH  # Column
        self.y = row * constants.GRID_HEIGHT  # Row
        self.rect = pygame.Rect(
            self.x, self.y, constants.GRID_WIDTH, constants.GRID_HEIGHT)
        self.colour = colour
        self.image = tile_images["grass"]
        self.path_tile_keys = [key for key in tile_images.keys() if key.startswith("FieldsTile_")]
        self.type = type
        self.path = "Open"  # Says if the shortest path exists using this path block
        self.neighbours = []  # All path blocks in 4 directions not diagonal

    def make_path(self):
        self.type = "Path"
        self.colour = "brown"
        self.image = tile_images[random.choice(self.path_tile_keys)]

    def make_obstacle(self):
        self.type = "Obstacle"

    def make_start(self):
        self.type = "Start"

    def make_end(self):
        self.type = "End"

    def make_open(self):
        self.path = "Open"

    def make_closed(self):
        self.path = "Closed"

    def update_neighbours(self, grid):
        self.neighbours = []

        if self.row < len(grid) - 1:
            down = grid[self.row + 1][self.col]
            if down.type != "Obstacle":
                self.neighbours.append(down)

        if self.row > 0:
            up = grid[self.row - 1][self.col]
            if up.type != "Obstacle":
                self.neighbours.append(up)

        if self.col < len(grid[0]) - 1:
            right = grid[self.row][self.col + 1]
            if right.type != "Obstacle":
                self.neighbours.append(right)

        if self.col > 0:
            left = grid[self.row][self.col - 1]
            if left.type != "Obstacle":
                self.neighbours.append(left)

    def __lt__(self, other):
        return False

    def draw(self):
        constants.WIN.blit(self.image, (self.rect.x, self.rect.y))
        # pygame.draw.rect(constants.WIN, self.colour, self.rect)
