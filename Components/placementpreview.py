import pygame

import Data.constants as constants
from Data.turret_types import turret_data

TRANSPERANT_MOUSE_RECT = pygame.Surface(
    (constants.GRID_WIDTH, constants.GRID_HEIGHT), pygame.SRCALPHA)
TRANSPERANT_MOUSE_RECT.fill((255, 255, 255, 75))


class PlacementPreview():
    def __init__(self):
        self.x = 0
        self.y = 0
        self.type = None
        self.display_range = False
        self.surface = TRANSPERANT_MOUSE_RECT
        self.range_surface = None
        self.range_surface_colour = (255, 255, 255, 75)
        self.current_obj_price = 0
        self.surface_rect = self.surface.get_rect()

    def create_translucent_obj(self, obj_type, block_selected, colour=False, display_range=False):
        self.surface = TRANSPERANT_MOUSE_RECT
        self.display_range = display_range
        self.type = obj_type

        if self.display_range:
            self.display_range = turret_data[block_selected]["turret_range"]
            self.current_obj_price = turret_data[block_selected]["price"]
            self.range_surface = pygame.Surface(
                (constants.GRID_WIDTH*self.display_range*2, constants.GRID_HEIGHT*self.display_range*2), pygame.SRCALPHA)

        if self.type == "Turret":
            turret_type = turret_data[block_selected]
            self.surface = pygame.Surface(
                (turret_type["width"], turret_type["height"]), pygame.SRCALPHA)

        elif self.type == "Block":
            self.surface = pygame.Surface(
                (constants.GRID_WIDTH, constants.GRID_HEIGHT), pygame.SRCALPHA)
            self.surface.fill((colour[0], colour[1], colour[2], 75))

        self.surface_rect = self.surface.get_rect()

    def loop(self, mouse_pos, coins, in_range):
        self.x = (mouse_pos[0] // constants.GRID_WIDTH)*constants.GRID_WIDTH
        self.y = (mouse_pos[1] // constants.GRID_HEIGHT)*constants.GRID_HEIGHT

        if self.range_surface != None:
            if coins >= self.current_obj_price and in_range:
                self.range_surface_colour = (0, 255, 0, 75)
            else:
                self.range_surface_colour = (255, 0, 0, 75)

    def draw(self):

        constants.WIN.blit(self.surface, (self.x, self.y))

        if self.display_range:
            turret_center_x = self.x + constants.GRID_WIDTH / 2
            turret_center_y = self.y + constants.GRID_HEIGHT / 2

            # Blit using top-left position derived from the center
            range_x = turret_center_x - self.range_surface.get_width() / 2
            range_y = turret_center_y - self.range_surface.get_height() / 2

            constants.WIN.blit(self.range_surface, (range_x, range_y))
            pygame.draw.circle(self.range_surface, self.range_surface_colour,
                               self.range_surface.get_rect().center, self.range_surface.get_width()/2)

        if self.type == "Turret":
            pygame.draw.circle(self.surface, (255, 0, 0, 75),
                               self.surface_rect.center, self.surface.get_width()/3)
            pygame.draw.line(self.surface, (255, 255, 255, 180),
                             self.surface_rect.center, (self.surface_rect.centerx, 0))

        elif self.type == "Block":
            constants.WIN.blit(self.surface, (self.x, self.y))

        # pygame.draw.rect(constants.WIN, "black", (self.x, self.y,
        #                  self.surface.get_width(), self.surface.get_height()), 4)
