import pygame
import Data.constants as constants
import Utils.UtilityFunction as UtilityFunction
import math
from Entities.bullets import Bullets


class Turrets():
    def __init__(self, x, y, width, height, image, damage, turret_range, velocity, frequency, price):
        self.rect = pygame.Rect(x, y, width, height)
        self.images = []
        for angle in range(0, 359):
            self.images.append(UtilityFunction.load_image(
                image, width*1.2, height*1.2, angle))
        self.attack = damage
        self.range = turret_range*constants.GRID_WIDTH
        self.vel = velocity
        self.bullets = []
        self.last_shot = 0
        self.frequency = frequency
        self.price = price

    def shoot(self, enemies, last_frame):
        self.last_shot += last_frame
        enemy = None
        for e in enemies:
            enemy = self.check_range(e)
            if enemy:
                break

        if self.last_shot >= self.frequency and enemy != None:
            angle = UtilityFunction.get_predictive_angle(
                self.rect.center, enemy, self.vel)

            bullet = Bullets(self.rect.centerx, self.rect.centery,
                             self.attack*0.7, self.attack*1.1, angle, self.vel, "red")

            self.bullets.append(bullet)
            self.last_shot = 0

    def check_range(self, target):
        target_obj = None
        range = math.sqrt(((target.rect.centerx - self.rect.centerx) **
                           2) + ((target.rect.centery - self.rect.centery) ** 2))
        if range <= self.range:
            target_obj = target

        return target_obj

    def loop(self, enemies, last_frame):
        self.shoot(enemies, last_frame)
        for bullet in self.bullets[:]:
            bullet.movement()

            # distance from turret to bullet
            bx, by = bullet.rect.center
            tx, ty = self.rect.center

            dist = math.dist((bx, by), (tx, ty))

            if dist > self.range:
                self.bullets.remove(bullet)

    def draw(self, enemies):
        # pygame.draw.rect(constants.WIN, "red", self.rect)
        target_pos = (0, 0)
        for enemy in enemies:
            target_pos = self.check_range(enemy)
            if target_pos:
                target_pos = target_pos.rect.center
                break
            else:
                target_pos = (0, 0)

        for bullet in self.bullets:
            bullet.draw()

        # pygame.draw.circle(constants.WIN, self.colour,
            #    self.rect.center, self.rect.width / 3)

        angle = -int(UtilityFunction.get_angle(
            target_pos, self.rect.center)-90) % 359
        image = self.images[angle]

        turret_surface_rect = image.get_rect()
        turret_surface_rect.center = self.rect.center
        constants.WIN.blit(image, turret_surface_rect)

        # end_point = UtilityFunction.move_at_angle(rotate, 19)

        # pygame.draw.line(constants.WIN, "white", self.rect.center,
        #  (self.rect.centerx - end_point[0], self.rect.centery - end_point[1]), 1)
