import random

from Entities.troops import Troops
from Data.enemy_types import enemy_data


class EnemyManager():
    def __init__(self, start_base, end_base, waypoints):
        self.enemies = []

        self.enemy_base = start_base  # Where enemy spawns
        self.home_base = end_base  # Base it's trying to attack

        self.waypoints = waypoints

        self.enemy_spawn_timer = 0
        self.enemy_spawn_delay = 3000

        self.enemy_created = lambda pos, current_id: Troops(
            pos[0], pos[1], self.home_base, self.waypoints, **enemy_data[current_id])

    def update(self, last_frame, turrets):
        self.enemy_spawn_timer += last_frame
        coins_earned = 0

        if not self.enemies:
            self.spawn_enemy()
        # if self.enemy_spawn_timer >= self.enemy_spawn_delay:
        #     self.spawn_enemy()
        #     self.enemy_spawn_timer = 0
        #     self.enemy_spawn_delay = max(400, self.enemy_spawn_delay - 10)

        for enemy in self.enemies[:]:
            enemy.loop(self.home_base, last_frame)

            for turret in turrets:
                for bullet in turret.bullets[:]:
                    if bullet.rect.colliderect(enemy.rect):
                        enemy.hit(turret.attack)
                        turret.bullets.remove(bullet)

            if enemy.health <= 0:
                coins_earned += enemy.loot
                self.enemies.remove(enemy)
                break

        return coins_earned

    def spawn_enemy(self):
        type_enemy = random.randint(1, 20)
        if type_enemy in enemy_data:
            enemy_obj = self.enemy_created(
                self.enemy_base.rect.center, type_enemy)
        else:
            enemy_obj = self.enemy_created(
                self.enemy_base.rect.center, 1)
        self.enemies.append(enemy_obj)

    def update_waypoints(self, waypoints, waypoint_gen):
        self.waypoints = waypoints
        for enemy in self.enemies:
            enemy.update_waypoints(waypoint_gen)

    def draw(self):
        for enemy in self.enemies:
            enemy.draw()
