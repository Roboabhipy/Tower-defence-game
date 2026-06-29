import pygame
import random
import constants
import pathfinder
from blocks import Blocks
from turrets import Turrets
from enemies import Enemy
from base import Base
from buttons import Buttons
from UtilityFunction import create_grid
from turret_types import turret_data
from enemy_types import enemy_data


def draw_grid():

    # Draws grid
    for i in range(constants.WIDTH // constants.GRID_WIDTH):
        pygame.draw.line(constants.WIN, "white", (i*constants.GRID_WIDTH,
                         0), (i*constants.GRID_WIDTH, constants.HEIGHT))
        for j in range(constants.HEIGHT // constants.GRID_HEIGHT):
            pygame.draw.line(constants.WIN, "white", (0, j*constants.GRID_HEIGHT),
                             (constants.WIDTH, j*constants.GRID_HEIGHT))


def draw_mouse_rect(mouse_grid_pos):
    transperant_rect = pygame.Surface(
        (constants.GRID_WIDTH, constants.GRID_HEIGHT), pygame.SRCALPHA)
    transperant_rect.fill((255, 255, 255, 75))
    constants.WIN.blit(
        transperant_rect, (mouse_grid_pos[0], mouse_grid_pos[1]))


def get_mouse_grid_pos(mouse_pos):
    mouse_grid_x = (
        mouse_pos[0] // constants.GRID_WIDTH)*constants.GRID_WIDTH
    mouse_grid_y = (
        mouse_pos[1] // constants.GRID_HEIGHT)*constants.GRID_HEIGHT
    return mouse_grid_x, mouse_grid_y


def enemy_loop(enemies, waypoint, turrets, home_base, enemy_count, enemy_types, enemy_base, coins, enemy_sp_count):
    enemy_spawn_count = enemy_sp_count
    for enemy in enemies[:]:
        enemy.movement(waypoint)
        if enemy.rect.colliderect(home_base.rect):
            enemy.attack_base(home_base, enemy_count)

        for turret in turrets:
            for bullet in turret.bullets[:]:
                if bullet.rect.colliderect(enemy.rect):
                    enemy.hit(turret.attack)
                    turret.bullets.remove(bullet)

        if enemy.health <= 0:
            coins += enemy.loot
            enemies.remove(enemy)

    if enemy_count >= enemy_spawn_count:
        type_enemy = random.randint(1, 20)
        if type_enemy in enemy_types:
            enemy_obj = enemy_obj = enemy_types[type_enemy](
                enemy_base.rect.center)
        else:
            enemy_obj = enemy_types[1](
                enemy_base.rect.center)
        enemies.append(enemy_obj)
        enemy_spawn_count -= 10
        enemy_spawn_count = max(400, enemy_spawn_count)
        enemy_count = 0

    return enemies, enemy_count, coins, enemy_spawn_count


def turret_loop(turrets, last_frame, enemies):
    for turret in turrets:
        turret.loop(enemies, last_frame)


def button_loop(buttons, mouse_pos):
    for button in buttons:
        button.mouse_detection(mouse_pos)


def place_block(blocks, turrets, block_selected, placers, map_cor, occupied_grid_cor, mouse_grid_pos, coins):
    # Deletes objects
    if block_selected == 4 and mouse_grid_pos in occupied_grid_cor:
        coins += 25
        blocks, turrets = remove_block(
            blocks, turrets, mouse_grid_pos, occupied_grid_cor)
        return blocks, turrets, coins

    # if mouse_grid_pos in map_cor:
    #     return blocks, turrets, coins

    if block_selected in placers:
        # turret_type = turret_data[block_selected]
        # if coins >= turret_type["price"]:
        #     coins -= turret_type["price"]
        obj = placers[block_selected](mouse_grid_pos)

        if mouse_grid_pos in occupied_grid_cor:
            blocks, turrets = remove_block(
                blocks, turrets, mouse_grid_pos, occupied_grid_cor)
        else:
            occupied_grid_cor.append(mouse_grid_pos)

        if isinstance(obj, Turrets):
            turrets.append(obj)
        else:
            blocks.append(obj)

    return blocks, turrets, coins


def remove_block(blocks, turrets, mouse_grid_pos, occupied_grid_cor):
    for cor in occupied_grid_cor[:]:
        if cor[0] == mouse_grid_pos[0] and cor[1] == mouse_grid_pos[1]:
            occupied_grid_cor.remove(cor)
            blocks[:] = [b for b in blocks if (
                b.rect.x, b.rect.y) != mouse_grid_pos]
            turrets[:] = [t for t in turrets if (
                t.rect.x, t.rect.y) != mouse_grid_pos]

    return blocks, turrets


def create_waypoint(map_cor, end_target=None):
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
    if waypoints is not None and end_target is not None:
        waypoints.append(end_target)

    return waypoints


def draw(turrets, blocks, enemies, map, buttons, mouse_grid_pos, coins):
    constants.WIN.fill("dark green")
    draw_mouse_rect(mouse_grid_pos)
    draw_grid()
    for cor in map:
        pygame.draw.rect(constants.WIN, "brown", (cor[0], cor[1], 50, 50))

    for turret in turrets:
        turret.draw(enemies)

    for block in blocks:
        block.draw()

    for enemy in enemies:
        enemy.draw()

    for button in buttons:
        button.draw()

    coin_text = constants.FONT.render('Coins: ' + str(coins), True, "white")
    constants.WIN.blit(coin_text, (10, 10))


def main():
    clock = pygame.time.Clock()
    run = True

    turrets = []
    blocks = []
    enemies = []
    enemy_count = 0

    occupied_grid_cor = []

    block_selected = 0

    placers = {
        1: lambda pos: Blocks(pos[0], pos[1], constants.GRID_WIDTH, constants.GRID_HEIGHT, "green"),
        2: lambda pos: Blocks(pos[0], pos[1], constants.GRID_WIDTH, constants.GRID_HEIGHT, "brown"),
        3: lambda pos: Blocks(pos[0], pos[1], constants.GRID_WIDTH, constants.GRID_HEIGHT, "red"),
        5: lambda pos: Turrets(pos[0], pos[1], **turret_data[5]),
        6: lambda pos: Turrets(pos[0], pos[1], **turret_data[6]),
        7: lambda pos: Turrets(pos[0], pos[1], **turret_data[7]),
        8: lambda pos: Turrets(pos[0], pos[1], **turret_data[8])
    }

    enemy_types = {
        1: lambda pos: Enemy(pos[0], pos[1], **enemy_data[1]),
        2: lambda pos: Enemy(pos[0], pos[1], **enemy_data[2]),
        3: lambda pos: Enemy(pos[0], pos[1], **enemy_data[3])
    }

    home_base = Base(1000, 650, 100, 100, "blue", 300)
    enemy_base = Base(50, 50, 100, 100, "red", 300)

    buttons = [
        Buttons(constants.WIDTH - 100, 20, 75, 50, 1, "Green", "grey"),
        Buttons(constants.WIDTH - 100, 100, 75, 50, 2, "Path", "grey"),
        Buttons(constants.WIDTH - 100, 180, 75, 50, 3, "Red", "grey"),
        Buttons(constants.WIDTH - 100, 260, 75, 50, 4, "Delete", "grey"),
        Buttons(constants.WIDTH - 100, 340, 75, 50, 5, "Tower", "grey"),
        Buttons(constants.WIDTH - 100, 420, 75, 50, 6, "Rapid", "grey"),
        Buttons(constants.WIDTH - 100, 500, 75, 50, 7, "Cannon", "grey"),
        Buttons(constants.WIDTH - 100, 580, 75, 50, 8, "Sniper", "grey"),
    ]

    coins = 100
    enemy_spawn_count = 3000

    map = create_grid(constants.GRID_WIDTH,
                      constants.WIDTH // constants.GRID_WIDTH)

    waypoint = create_waypoint(
        map, (home_base.rect.centerx - constants.GRID_WIDTH, home_base.rect.centery))

    while run:
        last_frame = clock.tick(constants.FPS)
        mouse_pos = pygame.mouse.get_pos()
        mouse_grid_pos = get_mouse_grid_pos(mouse_pos)
        enemy_count += last_frame

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                clicked_button = False
                for button in buttons:
                    if button.rect.collidepoint(mouse_pos):
                        clicked_button = True
                        block_selected = button.get_function()
                        break
                if not clicked_button:
                    blocks, turrets, coins = place_block(
                        blocks, turrets, block_selected, placers, constants.MAP_COR, occupied_grid_cor, mouse_grid_pos, coins)

        turret_loop(turrets, last_frame, enemies)

        enemies, enemy_count, coins, enemy_spawn_count = enemy_loop(
            enemies, waypoint, turrets, home_base, enemy_count, enemy_types, enemy_base, coins, enemy_spawn_count)

        button_loop(buttons, mouse_pos)
        draw(turrets, blocks, enemies, constants.MAP_COR,
             buttons, mouse_grid_pos, coins)

        home_base.draw()
        enemy_base.draw()
        for i in range(len(waypoint) - 1):
            pygame.draw.line(constants.WIN, "white",
                             waypoint[i], waypoint[i + 1], 3)
        pygame.display.update()
    print(occupied_grid_cor)
    pygame.quit()


if __name__ == "__main__":
    main()
