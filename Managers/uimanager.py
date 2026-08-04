import pygame

from Data.ui_types import build_data, troop_data
import Data.constants as constants

from UI.buttons import Buttons
from UI.menu import Menu

def create_buttons(menu, data):
    for button in data:
        menu.create_button(**data[button])


class UIManager():
    def __init__(self):
        self.menu = {}

        self.selected_menu = "Troop Shop"

        self.create_menu("Build Shop", 1050, 0)
        self.create_menu("Troop Shop", 1050, 0)
        create_buttons(self.menu["Troop Shop"], troop_data)
        create_buttons(self.menu["Build Shop"], build_data)
        
        
        self.show_menu = True
        self.menu_vis_button = Buttons(
            "->", "Menu vis", "#404859", "white", (1025, 25), None, 10, 50, 40)

    def create_menu(self, name, x, y, width=150, height=800, menu_col="black"):
        menu = Menu(x, y, name, width, height, menu_col)
        self.menu[name] = menu

    def get_function(self, mouse_pos):
        if self.menu_vis_button.base_rect.collidepoint(mouse_pos):
            if self.show_menu:
                self.menu_vis_button.base_rect.x = constants.WIDTH - self.menu_vis_button.base_rect.width
                self.show_menu = False
            else:
                self.menu_vis_button.base_rect.x = self.menu[self.selected_menu].rect.x - self.menu_vis_button.base_rect.width
                self.show_menu = True
            
            return 0, True
        
        if self.show_menu:        
            return self.menu[self.selected_menu].get_function(mouse_pos)
        
        return 0, False
        
    def loop(self, mouse_pos, coins=0):
        self.menu_vis_button.mouse_detection(mouse_pos, 0)
                
        if self.selected_menu != "" and self.show_menu:
            self.menu[self.selected_menu].loop(mouse_pos, coins)
            
        Buttons.hover()

    def draw(self):
        if self.selected_menu != "" and self.show_menu:
            self.menu[self.selected_menu].draw()

        self.menu_vis_button.draw()
