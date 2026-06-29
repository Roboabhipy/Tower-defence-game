import constants
import pygame


class Map():
    def __init__(self, col, row):
        self.row = row
        self.col = col
        self.x = col * constants.GRID_WIDTH  # Column
        self.y = row * constants.GRID_HEIGHT  # Row
        self.type = "Obstacle"
        self.path = "Open"  # Says if the shortest path exists using this path block
        self.neighbours = []  # All path blocks in 4 directions not diagonal

    def make_path(self):
        self.type = "Path"

    def make_obstacle(self):
        self.type = "Obstacle"
    
    def make_start(self):
        self.type = "Start"
    
    def make_end(self):
        self.type = "End"

    def make_open(self):
        self.path = "Open"

    def make_closed(self):
        self.path = "Closed"

    def update_neighbours(self, grid):
        self.neighbours = []
        print(len(grid))
        print(self.col, self.row)

        # Down
        if self.row < len(grid) -1 and not grid[self.row + 1][self.col] != "Obstacle":
            self.neighbours.append(grid[self.row + 1][self.col])

        # Up
        if self.row > len(grid) - 1 and not grid[self.row - 1][self.col] != "Obstacle":
            self.neighbours.append(grid[self.row - 1][self.col])

        # Right
        if self.col < len(grid) - 1 and not grid[self.row][self.col + 1] != "Obstacle":
            self.neighbours.append(grid[self.row][self.col + 1])

        # Left
        if self.col > len(grid) - 1 and not grid[self.row][self.col - 1] != "Obstacle":
            self.neighbours.append(grid[self.row][self.col - 1])
        
        # print(len(self.neighbours))
    
    def __lt__(self, other):
        return False
