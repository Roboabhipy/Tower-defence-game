import pygame

import Data.constants as constants

from UI.menu import Menu


class UIManager():
    def __init__(self):
        self.menu = {}

        self.selected_menu = "build"

        self.create_menu("build", 1050, 0)
        self.menu["build"].create_button("Tower", 5, "dark blue", "white", 50)
        self.menu["build"].create_button("Rapid", 6, "white", "black", 100)
        self.menu["build"].create_button("Cannon", 7, "white", "black", 350)
        self.menu["build"].create_button("Sniper", 8, "white", "black", 250)
        self.menu["build"].create_button("Path", 2, "white", "black", 250)
        self.menu["build"].create_button("Barrier", 1, "white", "black", 250)

    def create_menu(self, name, x, y, width=150, height=800, menu_col="black"):
        menu = Menu(x, y, width, height, menu_col)
        self.menu[name] = menu

    def loop(self, mouse_pos, coins=0):
        self.menu[self.selected_menu].loop(mouse_pos, coins)

    def draw(self):
        if self.selected_menu != "":
            self.menu[self.selected_menu].draw()
