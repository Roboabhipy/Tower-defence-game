import pygame

import Data.constants as constants

from UI.menu import Menu


class UIManager():
    def __init__(self):
        self.menu = {}

        self.selected_menu = "Build Shop"

        self.create_menu("Build Shop", 1050, 0)
        self.menu["Build Shop"].create_button("Tower", 6, 50)
        self.menu["Build Shop"].create_button("Rapid", 7, 100)
        self.menu["Build Shop"].create_button("Cannon", 8, 350)
        self.menu["Build Shop"].create_button("Sniper", 9, 250)
        self.menu["Build Shop"].create_button("Path", 3, 100)
        self.menu["Build Shop"].create_button("Barrier", 2, 250)
        self.menu["Build Shop"].create_button("Small Troop", 10, 100)
        self.menu["Build Shop"].create_button("Delete", 1, 0)

    def create_menu(self, name, x, y, width=150, height=800, menu_col="black"):
        menu = Menu(x, y, name, width, height, menu_col)
        self.menu[name] = menu

    def loop(self, mouse_pos, coins=0):
        self.menu[self.selected_menu].loop(mouse_pos, coins)

    def draw(self):
        if self.selected_menu != "":
            self.menu[self.selected_menu].draw()
