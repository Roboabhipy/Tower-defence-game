import pygame
import constants
from queue import PriorityQueue

# Finds approximate distance between current point and end


def h(crt, end):
    x1, y1 = crt
    x2, y2 = end
    return abs(x1 - x2) + abs(y1 - y2)


def get_node_center(node):
    return (node.x + constants.GRID_WIDTH / 2, node.y + constants.GRID_HEIGHT / 2)


def build_centerline_path(path_nodes):
    if not path_nodes:
        return []

    centerline = []
    prev_point = None

    for node in path_nodes:
        point = get_node_center(node)
        if prev_point is not None:
            midpoint = ((prev_point[0] + point[0]) / 2,
                        (prev_point[1] + point[1]) / 2)
            centerline.append(midpoint)
        else:
            centerline.append(point)
        prev_point = point

    return centerline


def reconstruct_path(came_from, current):
    path_nodes = [current]
    while current in came_from:
        current = came_from[current]
        path_nodes.append(current)

    path_nodes.reverse()
    return build_centerline_path(path_nodes)


def algorithm(paths, start, end):
    for row in paths:
        for spot in row:
            spot.update_neighbours(paths)

    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    came_from = {}

    g_score = {}
    f_score = {}
    for row in paths:
        for spot in row:
            g_score[spot] = float("inf")
            f_score[spot] = float("inf")

    g_score[start] = 0
    f_score[start] = h(get_node_center(start), get_node_center(end))

    open_set_hash = {start}

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None

        _, _, current = open_set.get()
        open_set_hash.remove(current)

        if current == end:
            return reconstruct_path(came_from, current)

        for neighbour in current.neighbours:
            temp_g_score = g_score[current] + 1

            if temp_g_score < g_score[neighbour]:
                came_from[neighbour] = current
                g_score[neighbour] = temp_g_score
                f_score[neighbour] = temp_g_score + \
                    h(get_node_center(neighbour), get_node_center(end))
                if neighbour not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighbour], count, neighbour))
                    open_set_hash.add(neighbour)
                    neighbour.make_open()

    return False
