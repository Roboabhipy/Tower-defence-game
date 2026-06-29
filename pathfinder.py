import pygame
import constants
from queue import PriorityQueue

# Finds approximate distance between current point and end


def h(crt, end):
    x1, y1 = crt
    x2, y2 = end
    return abs(x1 - x2) + abs(y1 - y2)


def reconstruct_path(came_from, current):
    waypoints = []
    while current in came_from:
        current = came_from[current]
        waypoints.append((current.x, current.y))

    waypoints.reverse()
    return waypoints


def algorithm(paths, start, end):
    for path in paths:
        for spot in path:
            print(spot)
            spot.update_neighbours(paths)
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    came_from = {}
    # Exact distance from start path block to any other block
    g_score = {path: float("inf") for path in paths}
    g_score[start] = 0

    # Predicted distance from start path block to any other block
    f_score = {path: float("inf") for path in paths}
    f_score[start] = h((start.x, start.y), (end.rect.centerx-constants.GRID_WIDTH, end.rect.centery))

    open_set_hash = {start}

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None

        current = open_set.get()[2]
        open_set_hash.remove(current)

        if current == end:
            waypoints = reconstruct_path(came_from, current)
            return waypoints

        for neighbour in current.neighbours:
            temp_g_score = g_score[current] + 1

            if temp_g_score < g_score[neighbour]:
                came_from[neighbour] = current
                g_score[neighbour] = temp_g_score
                f_score[neighbour] = temp_g_score + h((neighbour.x, neighbour.y), (end.rect.centerx-constants.GRID_WIDTH, end.rect.centery))
                if neighbour not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighbour], count, neighbour))
                    open_set_hash.add(neighbour)
                    neighbour.make_open()

    return False
