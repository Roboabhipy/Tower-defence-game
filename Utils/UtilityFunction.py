import math
import Data.constants as constants
from Entities.mapcreator import Map
import pygame
import os


image_cache = {}


def load_image(image, width, height, rotate):
    key = (image, width, height, rotate)
    if key not in image_cache:
        loading_image = pygame.image.load(
            os.path.join('Assets', image + ".png"))

        if rotate != 0:
            loaded_image = pygame.transform.rotate(
                pygame.transform.scale(loading_image, (width, height)), rotate)
        else:
            loaded_image = pygame.transform.scale(
                loading_image, (width, height))
        image_cache[key] = loaded_image
    return image_cache[key]


sprite_cache = {}


def load_sprite_sheets(dir1, dir2, width, height, loop_size, direction=False):
    key = (dir2, width, height)

    if key not in sprite_cache:
        path = os.path.join(dir1, dir2)
        images = [f for f in os.listdir(
            path) if os.path.isfile(os.path.join(path, f))]

        all_sprites = {}

        for image in images:
            sprite_sheet = pygame.image.load(
                os.path.join(path, image)).convert_alpha()
            sheet_width = sprite_sheet.get_width()
            sheet_height = sprite_sheet.get_height()

            sprites = []

            # Loop rows
            for y in range(0, sheet_height, loop_size):
                # Loop columns
                for x in range(0, sheet_width, loop_size):
                    surface = pygame.Surface(
                        (loop_size, loop_size), pygame.SRCALPHA)

                    rect = pygame.Rect(x, y, loop_size, loop_size)
                    surface.blit(sprite_sheet, (0, 0), rect)

                    surface = pygame.transform.scale(surface, (width, height))
                    sprites.append(surface)

            if direction:
                all_sprites[image.replace(".png", "") + "_right"] = sprites
                all_sprites[image.replace(
                    ".png", "") + "_left"] = flip(sprites)
            else:
                all_sprites[image.replace(".png", "")] = sprites

        sprite_cache[key] = all_sprites

    return sprite_cache[key]


def flip(sprites):
    return [pygame.transform.flip(sprite, True, False) for sprite in sprites]


def create_grid(rows):
    grid = []
    path_positions = {
        (x // constants.GRID_WIDTH, y // constants.GRID_HEIGHT)
        for x, y in constants.MAP_COR
    }

    for row in range(rows):
        grid.append([])
        for col in range(rows):
            spot = Map(col, row, "dark green")
            if (col, row) in path_positions:
                spot.make_path()
            grid[row].append(spot)
    return grid


def get_angle(pos_1, pos_2):
    x = pos_2[0] - pos_1[0]
    y = pos_2[1] - pos_1[1]
    rotate = math.degrees(math.atan2(y, x))
    return rotate


def polygon_points(x, y, width, height, angle_deg):
    angle = math.radians(angle_deg)
    cx, cy = x, y

    hw = width / 2
    hh = height / 2

    corners = [
        (-hw, -hh),
        (hw, -hh),
        (hw,  hh),
        (-hw,  hh)
    ]

    rotated = []
    for x, y in corners:
        rx = x * math.cos(angle) - y * math.sin(angle)
        ry = x * math.sin(angle) + y * math.cos(angle)
        rotated.append((cx + rx, cy + ry))

    return rotated


def move_at_angle(angle, distance):
    rad = math.radians(angle)
    x = math.cos(rad) * distance
    y = math.sin(rad) * distance
    return x, y


def get_predictive_angle(turret_pos, enemy_obj, bullet_speed):
    # 1. Get current positions
    tx, ty = turret_pos
    ex, ey = enemy_obj.rect.center

    # 2. Get enemy velocity
    vx = enemy_obj.vx
    vy = enemy_obj.vy

    # 3. Approximate travel time based on current distance
    distance = math.hypot((ex - tx), (ey - ty))
    travel_time = distance / bullet_speed

    # 4. Predict future position
    predicted_x = ex + (vx * travel_time)
    predicted_y = ey + (vy * travel_time)

    # 5. Calculate angle to the predicted spot
    dx = predicted_x - tx
    dy = predicted_y - ty
    return math.degrees(math.atan2(dy, dx))
