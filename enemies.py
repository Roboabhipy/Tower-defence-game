import pygame
import constants
import math
from health import Health


class Enemy():
    def __init__(self, x, y, waypoints, width, height, colour, health, attack, velocity, loot):
        self.rect = pygame.Rect(x, y, width, height)
        self.health_rect = Health(
            self.rect.centerx-15, self.rect.y - 15, 30, 5, health, health)
        self.colour = colour
        self.health = health
        self.attack = attack
        self.crt_wpt = 0
        self.vel = velocity
        self.loot = loot
        self.waypoints = waypoints
        self.vx = 0
        self.vy = 0
        self.health_rect.update_health(self.health)
        self.hit_count = 0

    def movement(self):
        # If we reached the final waypoint, stop
        if self.crt_wpt >= len(self.waypoints):
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
        if dist <= max(2, self.vel / 2):
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

    def hit(self, damage):
        self.health -= damage
        self.health_rect.update_health(self.health)

    def attack_base(self, base, last_frame):
        self.hit_count += last_frame
        if self.hit_count > 500:
            base.hit(self.attack)
            self.hit_count = 0

    def update_waypoints(self, waypoints):
        self.crt_wpt = 1
        self.waypoints = waypoints(self.rect.center)

    def draw(self):
        pygame.draw.rect(constants.WIN, self.colour, self.rect)
        pygame.draw.rect(constants.WIN, "red", self.health_rect.rect)
