import pygame

import Data.constants as constants
from Data.block_types import block_data
from Data.turret_types import turret_data
from Data.ally_types import ally_data

from Managers.enemymanager import EnemyManager
from Managers.mapmanager import MapManager
from Managers.uimanager import UIManager
from Managers.allymanager import AllyManager

from Entities.player import Player

from Components.placementpreview import PlacementPreview


def create_grid_surface():

    grid_surface = pygame.Surface(
        (constants.WIDTH, constants.HEIGHT), pygame.SRCALPHA)

    # Draws grid
    for i in range(0, constants.WIDTH, constants.GRID_WIDTH):
        pygame.draw.line(grid_surface, "white", (i,
                         0), (i, constants.HEIGHT))

    for j in range(0, constants.HEIGHT, constants.GRID_HEIGHT):
        pygame.draw.line(grid_surface, "white", (0, j),
                         (constants.WIDTH, j))

    return grid_surface


def get_mouse_grid_pos(mouse_pos):
    mouse_grid_x = (
        mouse_pos[0] // constants.GRID_WIDTH)*constants.GRID_WIDTH
    mouse_grid_y = (
        mouse_pos[1] // constants.GRID_HEIGHT)*constants.GRID_HEIGHT

    return mouse_grid_x, mouse_grid_y


def turret_loop(turrets, last_frame, enemies):
    for turret in turrets:
        turret.loop(enemies, last_frame)


def get_type(block_selected):
    selected_type = None
    display_range = False
    colour = False

    if block_selected == 1:
        selected_type = "Delete"

    if block_selected in block_data:
        selected_type = "Block"
        colour = block_data[block_selected]["colour"]

    elif block_selected in turret_data:
        selected_type = "Turret"
        display_range = True

    elif block_selected in ally_data:
        selected_type = "Ally"

    return selected_type, display_range, colour


def draw(grid_surface, mapmanager, player, enemies, uimanager, coins, allymanager, placementpreview):
    constants.WIN.fill("black")
    mapmanager.draw(enemies.enemies)

    constants.WIN.blit(grid_surface, (0, 0))

    enemies.draw()
    allymanager.draw()

    player.draw()
    placementpreview.draw()
    uimanager.draw()

    coin_text = constants.FONT.render('Coins: ' + str(coins), True, "white")
    constants.WIN.blit(coin_text, (10, 10))


def main():
    clock = pygame.time.Clock()
    run = True

    grid_surface = create_grid_surface()

    mapmanager = MapManager()

    enemymanager = EnemyManager(mapmanager.enemy_base,
                                mapmanager.home_base, mapmanager.current_waypoints)

    uimanager = UIManager()

    main_player = Player(mapmanager.home_base.rect.x,
                         mapmanager.home_base.rect.y, 40, 40, 10, 3, 2, mapmanager.occupied_grids)

    allymanager = AllyManager(
        mapmanager.home_base, mapmanager.enemy_base, mapmanager.create_waypoint)

    placementpreview = PlacementPreview()

    coins = 1000000000

    block_selected = 0

    while run:
        last_frame = clock.tick(constants.FPS)
        mouse_pos = pygame.mouse.get_pos()
        keys = pygame.key.get_pressed()
        mouse_grid_pos = get_mouse_grid_pos(mouse_pos)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                block_selected, clicked_button = uimanager.get_function(
                    mouse_pos)

                selected_type, display_range, block_colour = get_type(
                    block_selected)
                placementpreview.create_translucent_obj(
                    selected_type, block_selected, block_colour, display_range)

                if not clicked_button:
                    # in_range = main_player.check_range(mouse_grid_pos)
                    in_range = True
                    if in_range:
                        waypoints = False

                        if selected_type == "Delete":
                            coins += mapmanager.delete_obj(mouse_grid_pos)

                        elif selected_type in ("Block", "Turret"):
                            spent_coins, waypoints = mapmanager.place_block(
                                block_selected, mouse_grid_pos, coins)

                            coins -= spent_coins

                        elif selected_type == "Ally":
                            coins -= allymanager.create_ally(
                                coins, block_selected)

                        if waypoints:
                            enemymanager.update_waypoints(
                                waypoints, mapmanager.create_waypoint)

        main_player.loop(keys)

        turret_loop(mapmanager.turrets, last_frame, enemymanager.enemies)

        coins += enemymanager.update(last_frame, mapmanager.turrets)

        allymanager.update(last_frame, enemymanager.enemies)

        placementpreview.loop(mouse_pos)

        uimanager.loop(mouse_pos, coins)

        draw(grid_surface, mapmanager, main_player, enemymanager,
             uimanager, coins, allymanager, placementpreview)

        pygame.display.update()
    pygame.quit()


if __name__ == "__main__":
    main()
