import pygame
import constants

from buttons import Buttons

from enemymanager import EnemyManager
from mapmanager import MapManager
from player import Player


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


def turret_loop(turrets, last_frame, enemies):
    for turret in turrets:
        turret.loop(enemies, last_frame)


def button_loop(buttons, mouse_pos):
    for button in buttons:
        button.mouse_detection(mouse_pos)


def draw(mapmanager, player, enemies, buttons, mouse_grid_pos, coins):
    constants.WIN.fill("black")
    mapmanager.draw(enemies.enemies)

    draw_grid()
    draw_mouse_rect(mouse_grid_pos)

    enemies.draw()

    player.draw()
    for button in buttons:
        button.draw()

    coin_text = constants.FONT.render('Coins: ' + str(coins), True, "white")
    constants.WIN.blit(coin_text, (10, 10))


def main():
    clock = pygame.time.Clock()
    run = True

    mapmanager = MapManager()

    enemies = EnemyManager(mapmanager.enemy_base,
                           mapmanager.home_base, mapmanager.current_waypoints)

    main_player = Player(mapmanager.home_base.rect.x,
                         mapmanager.home_base.rect.y, 40, 40, 10, 3, 3)

    coins = 1000

    block_selected = 0

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

    while run:
        last_frame = clock.tick(constants.FPS)
        mouse_pos = pygame.mouse.get_pos()
        keys = pygame.key.get_pressed()
        mouse_grid_pos = get_mouse_grid_pos(mouse_pos)

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
                    in_range = main_player.check_range(mouse_grid_pos)
                    if in_range:
                        if block_selected == 4:
                            coins += mapmanager.delete_obj(mouse_grid_pos)

                        else:
                            spent_coins, waypoints = mapmanager.place_block(
                                block_selected, mouse_grid_pos, coins)

                            coins -= spent_coins

                            if waypoints:
                                def waypoint_gen(start, end=None): return mapmanager.create_waypoint(
                                    start, end, map_cor=None)
                                enemies.update_waypoints(
                                    waypoints, waypoint_gen)

        main_player.loop(keys)

        turret_loop(mapmanager.turrets, last_frame, enemies.enemies)

        coins += enemies.update(last_frame, mapmanager.turrets)

        button_loop(buttons, mouse_pos)
        draw(mapmanager, main_player, enemies,
             buttons, mouse_grid_pos, coins)

        pygame.display.update()
    pygame.quit()


if __name__ == "__main__":
    main()
