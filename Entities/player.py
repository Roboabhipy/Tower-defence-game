import Data.constants as constants
import pygame
import math
from Utils.UtilityFunction import load_sprite_sheets


class Player:
    def __init__(self, x, y, width, height, health, vel, build_range):
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

    def movement(self, keys):
        self.x_vel = 0
        self.y_vel = 0
        if keys[pygame.K_w] and self.rect.y >= 0:
            self.rect.y -= self.vel
            self.y_vel = -self.vel
        if keys[pygame.K_s] and self.rect.y < constants.HEIGHT - self.rect.height:
            self.rect.y += self.vel
            self.y_vel = self.vel
        if keys[pygame.K_d] and self.rect.x < constants.WIDTH - self.rect.width:
            self.rect.x += self.vel
            self.x_vel = self.vel
            if self.direction != "right":
                self.direction = "right"
                self.animation_count = 0
        if keys[pygame.K_a] and self.rect.x > 0:
            self.rect.x -= self.vel
            self.x_vel = -self.vel
            if self.direction != "left":
                self.direction = "left"
                self.animation_count = 0

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

    def draw(self):
        constants.WIN.blit(self.sprite, (self.rect.x, self.rect.y))
