import Data.constants as constants
import Utils.pathfinder as pathfinder
from Entities.mapcreator import Map
from Entities.turrets import Turrets
from Data.turret_types import turret_data
from Utils.UtilityFunction import create_grid
from Entities.base import Base


class MapManager:
    def __init__(self):
        self.occupied_grids = create_grid(
            constants.WIDTH // constants.GRID_WIDTH, Map)

        self.blocks = []
        self.turrets = []

        self.home_base = Base(950, 650, 50, 50, "blue", 300)
        self.enemy_base = Base(50, 100, 50, 50, "red", 300)

        self.current_waypoints = self.create_waypoint(
            self.enemy_base.rect.center, (self.home_base.rect.x, self.home_base.rect.centery), None)

        self.block_placers = {
            2: lambda pos: Map(pos[0] // constants.GRID_WIDTH, pos[1] // constants.GRID_HEIGHT, "green"),
            3: lambda pos: Map(pos[0] // constants.GRID_WIDTH, pos[1] // constants.GRID_HEIGHT, "brown", "Path"),
            4: lambda pos: Map(pos[0] // constants.GRID_WIDTH, pos[1] // constants.GRID_HEIGHT, "red")
        }

        self.turret_placers = lambda pos, id: Turrets(
            pos[0], pos[1], **turret_data[id])

#         self.waypoint_text = []
#         i = 0
#         for waypoint in self.current_waypoints:
#             i += 1
#             text = constants.FONT.render(str(i), True, "black")
#             self.waypoint_text.append((text, waypoint[0], waypoint[1]))

    def place_block(self, block_selected, mouse_pos, coins):

        clicked_column = mouse_pos[0] // constants.GRID_WIDTH
        clicked_row = mouse_pos[1] // constants.GRID_HEIGHT

        spent_coins = 0
        turret_obj = None
        obj = Map(
            clicked_column, clicked_row, "dark green")

        clicked_obj = self.occupied_grids[clicked_row][clicked_column]

        if clicked_obj.type in ("Start", "End"):
            return spent_coins, False

        if block_selected in self.block_placers:
            obj = self.block_placers[block_selected](mouse_pos)

        elif block_selected in turret_data:
            turret_price = turret_data[block_selected]["price"]
            if coins >= turret_price:
                turret_obj = self.turret_placers(mouse_pos, block_selected)

        new_waypoints = self.is_valid_placement(
            clicked_row, clicked_column, obj)

        if new_waypoints:
            self.occupied_grids[clicked_row][clicked_column] = obj
            if turret_obj:
                self.replace_obj(mouse_pos)
                spent_coins += turret_price
                self.turrets.append(turret_obj)

            path_changed = new_waypoints != self.current_waypoints

            if path_changed:
                self.current_waypoints = new_waypoints
                return spent_coins, new_waypoints

        return spent_coins, False

    def is_valid_placement(self, clicked_row, clicked_column, obj):

        temp_occupied_grids = [row[:] for row in self.occupied_grids]
        temp_occupied_grids[clicked_row][clicked_column] = obj

        waypoints = self.create_waypoint(
            self.enemy_base.rect.center, (self.home_base.rect.x, self.home_base.rect.centery), temp_occupied_grids)

        return waypoints

    def delete_obj(self, mouse_pos):
        coins_earned = 0

        clicked_column = mouse_pos[0] // constants.GRID_WIDTH
        clicked_row = mouse_pos[1] // constants.GRID_HEIGHT

        for turret in self.turrets[:]:
            if (turret.rect.x, turret.rect.y) == mouse_pos:
                coins_earned += int(turret.price * 0.45)
                self.turrets.remove(turret)
                break

        obj = Map(
            clicked_column, clicked_row, "dark green")
        new_waypoints = self.is_valid_placement(
            clicked_row, clicked_column, obj)

        if new_waypoints:
            for grid in self.occupied_grids[:]:
                for block in grid:
                    if (block.rect.x, block.rect.y) == mouse_pos and block.type not in ("Start", "End"):
                        block.type = "Obstacle"
                        block.colour = "dark green"
                        break

        return coins_earned

    def replace_obj(self, mouse_pos):
        for turret in self.turrets[:]:
            if (turret.rect.x, turret.rect.y) == mouse_pos:
                self.turrets.remove(turret)
                break

    def create_waypoint(self, start_coords, end_target, map_cor=None):
        if map_cor == None:
            map_cor = self.occupied_grids
        start_coords = (start_coords[0] // constants.GRID_WIDTH,
                        start_coords[1] // constants.GRID_HEIGHT)
        end_coords = end_target
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

        self.home_base.draw()
        self.enemy_base.draw()

        for turret in self.turrets:
            turret.draw(enemies)

#         for text in self.waypoint_text:
#             constants.WIN.blit(text[0], (text[1], text[2]))
