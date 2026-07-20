
from Entities.troops import Troops
from Data.ally_types import ally_data


class AllyManager():
    def __init__(self, start_base, end_base, waypoint_creator):
        self.allies = []

        self.spawn_base = start_base  # Where troop spawns
        self.target_base = end_base  # Base it's trying to attack

        self.create_waypoints = waypoint_creator
        self.waypoints = self.create_waypoints(
            self.spawn_base.rect.center, (self.target_base.rect.centerx, self.target_base.rect.bottom))

        self.enemy_created = lambda current_id: Troops(
            self.spawn_base.rect.x, self.spawn_base.rect.centery, self.target_base, self.waypoints, **ally_data[current_id])

    def update(self, last_frame, enemies):
        coins_earned = 0

        for ally in self.allies[:]:

            for enemy in enemies:
                if ally.rect.colliderect(enemy.rect):
                    ally.attack(last_frame, enemy)
                    enemy.attack(last_frame, ally)

            ally.loop(self.target_base, last_frame)

            if ally.health <= 0:
                coins_earned += ally.loot
                self.allies.remove(ally)
                break

        return coins_earned

    def create_ally(self, coins, type):
        spent_coins = 0
        if type in ally_data:
            price = ally_data[type]["price"]
            if coins >= price:
                spent_coins = price
                ally = self.enemy_created(type)
                self.allies.append(ally)

        return spent_coins

    def update_waypoints(self, waypoints, waypoint_gen):
        self.waypoints = waypoints
        for ally in self.allies:
            ally.update_waypoints(waypoint_gen)

    def draw(self):
        for ally in self.allies:
            ally.draw()
