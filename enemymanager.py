import random

from enemies import Enemy
from enemy_types import enemy_data


class EnemyManager():
    def __init__(self, start_base, end_base, waypoints):
        self.enemies = []

        self.enemy_base = start_base  # Where enemy spawns
        self.home_base = end_base  # Base it's trying to attack

        self.waypoints = waypoints

        self.enemy_spawn_timer = 0
        self.enemy_spawn_delay = 3000

        self.enemy_types = {
            1: lambda pos: Enemy(pos[0], pos[1], self.waypoints, **enemy_data[1]),
            2: lambda pos: Enemy(pos[0], pos[1], self.waypoints, **enemy_data[2]),
            3: lambda pos: Enemy(pos[0], pos[1], self.waypoints, **enemy_data[3])
        }

    def update(self, last_frame, turrets):
        self.enemy_spawn_timer += last_frame
        coins_earned = 0

        if self.enemy_spawn_timer >= self.enemy_spawn_delay:
            self.spawn_enemy()
            self.enemy_spawn_timer = 0
            self.enemy_spawn_delay = max(400, self.enemy_spawn_delay - 10)

        for enemy in self.enemies[:]:
            enemy.movement()
            if enemy.rect.colliderect(self.home_base.rect):
                enemy.attack_base(self.home_base, last_frame)

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
        if type_enemy in self.enemy_types:
            enemy_obj = self.enemy_types[type_enemy](
                self.enemy_base.rect.center)
        else:
            enemy_obj = self.enemy_types[1](
                self.enemy_base.rect.center)
        self.enemies.append(enemy_obj)

    def update_waypoints(self, waypoints, waypoint_gen):
        self.waypoints = waypoints
        for enemy in self.enemies:
            enemy.update_waypoints(waypoint_gen)

    def draw(self):
        for enemy in self.enemies:
            enemy.draw()
        
        self.home_base.draw()
        self.enemy_base.draw()
