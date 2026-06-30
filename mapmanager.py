import constants
from mapcreator import Map
from turrets import Turrets
from turret_types import turret_data
from UtilityFunction import create_grid


class MapManager:
    def __init__(self):
        self.occupied_grids = [create_grid(
            constants.WIDTH // constants.GRID_WIDTH)]
        self.blocks = []
        self.turrets = []

        self.block_placers = {
            1: lambda pos: Map(pos[0] // constants.GRID_WIDTH, pos[1] // constants.GRID_HEIGHT, "green"),
            2: lambda pos: Map(pos[0] // constants.GRID_WIDTH, pos[1] // constants.GRID_HEIGHT, "brown", "Path"),
            3: lambda pos: Map(pos[0] // constants.GRID_WIDTH, pos[1] // constants.GRID_HEIGHT, "red")
        }

        self.turret_placers = {5: lambda pos: Turrets(pos[0], pos[1], **turret_data[5]),
                               6: lambda pos: Turrets(pos[0], pos[1], **turret_data[6]),
                               7: lambda pos: Turrets(pos[0], pos[1], **turret_data[7]),
                               8: lambda pos: Turrets(pos[0], pos[1], **turret_data[8])
                               }

    def place_block(self, block_selected, mouse_pos, coins):
        spent_coins = 0
        if block_selected in self.block_placers:
            obj = self.block_placers[block_selected](mouse_pos)
            self.delete_obj(mouse_pos)
            self.occupied_grids.append(obj)

        elif block_selected in self.turret_placers:
            turret_price = turret_data[block_selected]["price"]
            if coins >= turret_price:
                spent_coins += turret_price
                obj = self.turret_placers[block_selected](mouse_pos)
                self.delete_obj(mouse_pos)
                self.turrets.append(obj)

        return spent_coins

    def delete_obj(self, mouse_pos):
        coins_earned = 0
        for turret in self.turrets[:]:
            if (turret.rect.x, turret.rect.y) == mouse_pos:
                coins_earned += int(turret.price * 0.45)
                self.turrets.remove(turret)
                break

        for block in self.occupied_grids[:]:
            if (block.rect.x, block.rect.y) == mouse_pos:
                self.turrets.remove(turret)
                break

        return coins_earned

    def draw(self):
        for obj in self.occupied_grids:
            obj.draw()
