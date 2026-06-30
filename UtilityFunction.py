import math
import constants
from mapcreator import Map


def create_grid(rows):
    grid = []
    path_positions = {
        (x // constants.GRID_WIDTH, y // constants.GRID_HEIGHT)
        for x, y in constants.MAP_COR
    }

    for row in range(rows):
        grid.append([])
        for col in range(rows):
            spot = Map(col, row, "brown", "Path")
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
