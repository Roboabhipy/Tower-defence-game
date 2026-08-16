import pygame
import Data.constants as constants
import math
from Components.health import Health
from Utils.UtilityFunction import load_sprite_sheets


class Troops():
    def __init__(self, x, y, target_base, waypoints, width, height, colour, health, attack, velocity, sprite, sprite_sheet_size, only_flip="All", has_direction=False, loot=False, price=False):
        self.rect = pygame.Rect(x, y, width, height)
        self.health_rect = Health(
            self.rect.centerx-15, self.rect.y - 15, 30, 5, health, health)
        self.colour = colour
        self.health = health
        self.attack_dmg = attack
        self.crt_wpt = 0
        self.vel = velocity
        self.loot = loot
        self.price = price
        self.waypoints = waypoints
        self.vx = 0
        self.vy = 0
        self.health_rect.update_health(self.health)
        self.hit_count = 1001
        self.attack_count = 0
        self.attack_animation_count = 0
        self.target_base = target_base
        self.direction = "right"
        self.animation_count = 0
        self.sprite_image = load_sprite_sheets(
            "Assets", sprite, width*1.5, height*1.5, sprite_sheet_size, only_flip)
        # Hardcoded just in case troop is created after loop function has been called
        self.sprite = self.sprite_image["idle_left"][0]
        self.has_directions = has_direction
        self.animation_delay = 3
        self.attacking = False

    def movement(self):
        # If we reached the final waypoint, stop
        if self.crt_wpt >= len(self.waypoints) or self.attacking:
            self.vx = 0
            self.vy = 0
            return

        # Get enemy center
        ex, ey = self.rect.center

        # Get current waypoint target
        wx, wy = self.waypoints[self.crt_wpt]

        # Compute direction vector
        dx = wx - ex
        dy = wy - ey

        # Compute distance to waypoint
        dist = math.hypot(dx, dy)

        # If close enough, snap to the waypoint and move to the next one
        if dist <= max(5, self.vel / 2):
            self.rect.centerx = wx
            self.rect.centery = wy
            self.health_rect.rect.x = self.rect.centerx - 15
            self.health_rect.rect.y = self.rect.y - 15
            self.crt_wpt += 1
            self.vx = 0
            self.vy = 0
            return

        dx /= dist
        dy /= dist

        self.vx = dx * self.vel
        self.vy = dy * self.vel

        # Move enemy so the center of the rectangle follows the waypoint path
        self.rect.centerx += self.vx
        self.rect.centery += self.vy
        self.health_rect.move(self.vx, self.vy)

    def handle_sprite_direction(self):
        self.sprite_sheet = "idle"
        if self.hit_count <= 500:
            self.sprite_sheet = "hit"
        elif self.attack_animation_count >= 500:
            self.sprite_sheet = "attack"
        elif self.vx != 0 or self.vy != 0:
            self.sprite_sheet = "run"

        if self.vx > 0 and self.direction != "right":
            self.direction = "right"
            self.animation_count = 0

        elif self.vx < 0 and self.direction != "left":
            self.direction = "left"
            self.animation_count = 0

        elif self.vy < 0 and self.direction != "down":
            self.direction = "down"
            self.animation_count = 0

        elif self.vy > 0 and self.direction != "up":
            self.direction = "up"
            self.animation_count = 0

        elif self.vx == 0 and self.vy == 0 and self.direction != "right":
            self.direction = "right"
            self.animation_count = 0

    def update_sprite(self):
        sprite_sheet_name = self.sprite_sheet + "_" + self.direction
        sprites = self.sprite_image[sprite_sheet_name]
        sprite_index = (self.animation_count //
                        self.animation_delay) % len(sprites)
        self.sprite = sprites[sprite_index]
        self.sprite.get_rect().center = self.rect.center
        self.animation_count += 1

    def hit(self, damage):
        self.hit_count = 0
        self.health -= damage
        self.health_rect.update_health(self.health)

    def attack(self, last_frame, target):
        self.attacking = True
        self.attack_count += last_frame
        self.attack_animation_count += last_frame
        if self.attack_count > 500:
            target.hit(self.attack_dmg)
            self.attack_count = 0

        if self.attack_animation_count >= 600:
            self.attack_animation_count = 0

        # self.attacking = False

    def update_waypoints(self, waypoints):
        self.crt_wpt = 1
        self.waypoints = waypoints(
            self.rect.center, (self.target_base.rect.x, self.target_base.rect.centery))

    def loop(self, base, last_frame):
        self.movement()
        if self.rect.colliderect(base.rect):
            self.attack(last_frame, base)

        self.hit_count += last_frame

        self.handle_sprite_direction()
        self.update_sprite()
        self.attacking = False

    def draw(self):
        #         pygame.draw.rect(constants.WIN, self.colour, self.rect)
        sprite_surface_rect = self.sprite.get_rect()
        sprite_surface_rect.center = self.rect.center
        constants.WIN.blit(self.sprite, sprite_surface_rect)
        self.health_rect.draw()
