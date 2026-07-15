import pygame

import Data.constants as constants

from UI.menu import Menu


class UIManager():
    def __init__(self):
        self.menu = {}

        self.selected_menu = "build"

        self.create_menu("build", 1050, 0)
        self.menu["build"].create_button("Tower", 5, "#404859", "white", 50)
        self.menu["build"].create_button("Rapid", 6, "#404859", "white", 100)
        self.menu["build"].create_button("Cannon", 7, "#404859", "white", 350)
        self.menu["build"].create_button("Sniper", 8, "#404859", "white", 250)
        self.menu["build"].create_button("Path", 2, "#404859", "white", 250)
        self.menu["build"].create_button("Barrier", 1, "#404859", "white", 250)
        self.menu["build"].create_button("Delete", 4, "#404859", "white", 0)

    def create_menu(self, name, x, y, width=150, height=800, menu_col="black"):
        menu = Menu(x, y, width, height, menu_col)
        self.menu[name] = menu

    def loop(self, mouse_pos, coins=0):
        self.menu[self.selected_menu].loop(mouse_pos, coins)

    def draw(self):
        if self.selected_menu != "":
            self.menu[self.selected_menu].draw()
