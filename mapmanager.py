import constants
import pathfinder
from mapcreator import Map
from turrets import Turrets
from turret_types import turret_data
from UtilityFunction import create_grid


class MapManager:
    def __init__(self):
        self.occupied_grids = create_grid(
            constants.WIDTH // constants.GRID_WIDTH)
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
        clicked_column = mouse_pos[0] // constants.GRID_WIDTH
        clicked_row = mouse_pos[1] // constants.GRID_HEIGHT
        spent_coins = 0
        obj = Map(
            clicked_column, clicked_row, "dark green")

        if block_selected in self.block_placers or block_selected in self.turret_placers:
            temp_occupied_grids = [row[:] for row in self.occupied_grids]
            turret_obj = False
            if block_selected in self.block_placers:
                obj = self.block_placers[block_selected](mouse_pos)

            elif block_selected in self.turret_placers:
                turret_price = turret_data[block_selected]["price"]
                if coins >= turret_price:
                    turret_obj = self.turret_placers[block_selected](mouse_pos)
                    obj = Map(
                        clicked_column, clicked_row, "dark green")

            temp_occupied_grids[clicked_row][clicked_column] = obj

            waypoints = self.create_waypoint(temp_occupied_grids)

            if waypoints:
                self.occupied_grids[clicked_row][clicked_column] = obj
                if turret_obj:
                    spent_coins += turret_price
                    self.delete_obj(mouse_pos)
                    self.turrets.append(turret_obj)

                print("placed")

        return spent_coins, waypoints

    def delete_obj(self, mouse_pos):
        coins_earned = 0
        for turret in self.turrets[:]:
            if (turret.rect.x, turret.rect.y) == mouse_pos:
                coins_earned += int(turret.price * 0.45)
                self.turrets.remove(turret)
                break

        for obj in self.occupied_grids[:]:
            for block in obj:
                if (block.rect.x, block.rect.y) == mouse_pos:
                    block.type = "Obstacle"
                    block.colour = "dark green"
                    break

        return coins_earned

    def create_waypoint(self, map_cor, end_target=None):
        start_coords = constants.MAP_COR[0]
        start_coords = (start_coords[0] // constants.GRID_WIDTH,
                        start_coords[1] // constants.GRID_HEIGHT)
        end_coords = constants.MAP_COR[-1]
        end_coords = (end_coords[0] // constants.GRID_WIDTH,
                      end_coords[1] // constants.GRID_HEIGHT)
        start = map_cor[start_coords[1]][start_coords[0]]
        end = map_cor[end_coords[1]][end_coords[0]]
        start.make_start()
        end.make_end()

        waypoints = pathfinder.algorithm(map_cor, start, end)
        if waypoints is not False and end_target is not None:
            waypoints.append(end_target)

        return waypoints

    def draw(self, enemies):
        for list in self.occupied_grids:
            for obj in list:
                obj.draw()

        for turret in self.turrets:
            turret.draw(enemies)
