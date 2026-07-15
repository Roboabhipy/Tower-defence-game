import pygame
import Data.constants as constants

from Managers.enemymanager import EnemyManager
from Managers.mapmanager import MapManager
from Entities.player import Player
from Managers.uimanager import UIManager

TRANSPERANT_MOUSE_RECT = pygame.Surface(
    (constants.GRID_WIDTH, constants.GRID_HEIGHT), pygame.SRCALPHA)
TRANSPERANT_MOUSE_RECT.fill((255, 255, 255, 75))


def draw_grid():

    # Draws grid
    for i in range(constants.WIDTH // constants.GRID_WIDTH):
        pygame.draw.line(constants.WIN, "white", (i*constants.GRID_WIDTH,
                         0), (i*constants.GRID_WIDTH, constants.HEIGHT))
        for j in range(constants.HEIGHT // constants.GRID_HEIGHT):
            pygame.draw.line(constants.WIN, "white", (0, j*constants.GRID_HEIGHT),
                             (constants.WIDTH, j*constants.GRID_HEIGHT))


def draw_mouse_rect(mouse_grid_pos):
    constants.WIN.blit(
        TRANSPERANT_MOUSE_RECT, (mouse_grid_pos[0], mouse_grid_pos[1]))


def get_mouse_grid_pos(mouse_pos):
    mouse_grid_x = (
        mouse_pos[0] // constants.GRID_WIDTH)*constants.GRID_WIDTH
    mouse_grid_y = (
        mouse_pos[1] // constants.GRID_HEIGHT)*constants.GRID_HEIGHT
    return mouse_grid_x, mouse_grid_y


def turret_loop(turrets, last_frame, enemies):
    for turret in turrets:
        turret.loop(enemies, last_frame)


def draw(mapmanager, player, enemies, uimanager, mouse_grid_pos, coins):
    constants.WIN.fill("black")
    mapmanager.draw(enemies.enemies)

    draw_grid()
    draw_mouse_rect(mouse_grid_pos)

    enemies.draw()

    player.draw()

    uimanager.draw()

    coin_text = constants.FONT.render('Coins: ' + str(coins), True, "white")
    constants.WIN.blit(coin_text, (10, 10))


def main():
    clock = pygame.time.Clock()
    run = True

    mapmanager = MapManager()

    enemies = EnemyManager(mapmanager.enemy_base,
                           mapmanager.home_base, mapmanager.current_waypoints)

    uimanager = UIManager()

    main_player = Player(mapmanager.home_base.rect.x,
                         mapmanager.home_base.rect.y, 40, 40, 10, 3, 2)

    coins = 1000

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
                block_selected, clicked_button = uimanager.menu["build"].get_function(
                    mouse_pos)

                if not clicked_button:
                    in_range = main_player.check_range(mouse_grid_pos)
                    if in_range:
                        if block_selected == 4:
                            coins += mapmanager.delete_obj(mouse_grid_pos)

                        else:
                            spent_coins, waypoints = mapmanager.place_block(
                                block_selected, mouse_grid_pos, coins)

                            coins -= spent_coins

                            if waypoints:
                                print("waypoint change")
                                def waypoint_gen(start, end=None): return mapmanager.create_waypoint(
                                    start, end, map_cor=None)
                                enemies.update_waypoints(
                                    waypoints, waypoint_gen)

        main_player.loop(keys)

        turret_loop(mapmanager.turrets, last_frame, enemies.enemies)

        coins += enemies.update(last_frame, mapmanager.turrets)

        uimanager.loop(mouse_pos, coins)
        draw(mapmanager, main_player, enemies,
             uimanager, mouse_grid_pos, coins)

        pygame.display.update()
    pygame.quit()


if __name__ == "__main__":
    main()
