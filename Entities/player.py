import Data.constants as constants
import pygame
import math
from Utils.UtilityFunction import load_sprite_sheets


class Player:
    def __init__(self, x, y, width, height, health, vel, build_range, grid):
        self.rect = pygame.Rect(x, y, width, height)
        self.vel = vel
        self.build_range = build_range
        self.health = health
        self.hit = False
        self.direction = "right"
        self.animation_count = 0
        self.sprite_image = load_sprite_sheets(
            "Assets", "VirtualGuy", width, height, 32, True)
        self.animation_delay = 3
        self.grid = grid
        self.pos_limit = self.calculate_pos_limit()

    def movement(self, keys):
        self.x_vel = 0
        self.y_vel = 0

        self.moved = False

        if self.pos_limit["up"]:
            if keys[pygame.K_w] and self.rect.y > self.pos_limit["up"]:
                self.moved = True
                self.y_vel = -self.vel

        if self.pos_limit["down"]:
            if keys[pygame.K_s] and self.rect.y < self.pos_limit["down"] - self.rect.height:
                self.moved = True
                self.y_vel = self.vel

        if self.pos_limit["right"]:
            if keys[pygame.K_d] and self.rect.x < self.pos_limit["right"] - self.rect.width:
                self.moved = True
                self.x_vel = self.vel

                if self.direction != "right":
                    self.direction = "right"
                    self.animation_count = 0

        if self.pos_limit["left"]:
            if keys[pygame.K_a] and self.rect.x > self.pos_limit["left"]:
                self.moved = True
                self.x_vel = -self.vel

                if self.direction != "left":
                    self.direction = "left"
                    self.animation_count = 0

        if self.moved:
            self.rect.x += self.x_vel
            self.rect.y += self.y_vel

    def calculate_pos_limit(self):
        neighbours = self.update_neighbours()
        pos_limit = {"left": None, "right": None, "up": None, "down": None}

        row = self.rect.y // constants.GRID_HEIGHT
        col = self.rect.x // constants.GRID_WIDTH

        # If the player is currently on a Path tile, allow them to move within it
        if 0 <= row < len(self.grid) and 0 <= col < len(self.grid[0]):
            current_tile = self.grid[row][col]
            if current_tile.type == "Path":
                pos_limit["left"] = current_tile.x
                pos_limit["right"] = current_tile.x + constants.GRID_WIDTH
                pos_limit["up"] = current_tile.y
                pos_limit["down"] = current_tile.y + constants.GRID_HEIGHT

        # Extend limits if adjacent neighbor tiles are also paths
        if neighbours["left"]:
            pos_limit["left"] = neighbours["left"].x

        if neighbours["right"]:
            pos_limit["right"] = neighbours["right"].x + constants.GRID_WIDTH

        if neighbours["up"]:
            pos_limit["up"] = neighbours["up"].y

        if neighbours["down"]:
            pos_limit["down"] = neighbours["down"].y + constants.GRID_HEIGHT

        return pos_limit

    def update_neighbours(self):
        neighbours = {}

        row = self.rect.y // constants.GRID_HEIGHT
        col = self.rect.x // constants.GRID_WIDTH

        left = False
        right = False
        up = False
        down = False

        if row < len(self.grid) - 1:
            if self.grid[row + 1][col].type == "Path":
                down = self.grid[row + 1][col]

        if row > 0:
            if self.grid[row - 1][col].type == "Path":
                up = self.grid[row - 1][col]

        if col < len(self.grid[0]) - 1:
            if self.grid[row][col + 1].type == "Path":
                right = self.grid[row][col + 1]

        if col > 0:
            if self.grid[row][col - 1].type == "Path":
                left = self.grid[row][col - 1]

        neighbours["left"] = left
        neighbours["right"] = right
        neighbours["up"] = up
        neighbours["down"] = down

        return neighbours

    def update_sprite(self):
        sprite_sheet = "idle"
        if self.hit:
            sprite_sheet = "hit"
        elif self.x_vel != 0 or self.y_vel != 0:
            sprite_sheet = "run"

        sprite_sheet_name = sprite_sheet + "_" + self.direction
        sprites = self.sprite_image[sprite_sheet_name]
        sprite_index = (self.animation_count //
                        self.animation_delay) % len(sprites)
        self.sprite = sprites[sprite_index]
        self.animation_count += 1

    def check_range(self, pos):
        x_distance = pos[0] - \
            ((self.rect.x // constants.GRID_WIDTH)*constants.GRID_WIDTH)
        y_distance = pos[1] - \
            ((self.rect.y // constants.GRID_HEIGHT)*constants.GRID_HEIGHT)
        distance = math.hypot(x_distance, y_distance)
        distance = (distance // constants.GRID_WIDTH)

        if distance <= self.build_range:
            return True

        return False

    def loop(self, keys):
        self.movement(keys)
        self.update_sprite()

        if self.moved:
            self.pos_limit = self.calculate_pos_limit()

    def draw(self):
        # pygame.draw.rect(constants.WIN, "red", self.rect)
        constants.WIN.blit(self.sprite, (self.rect.x, self.rect.y))
