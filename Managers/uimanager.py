from UI.menu import Menu
from Data.ui_types import ui_data


def create_buttons(menu):
    for button in ui_data:
        menu.create_button(**ui_data[button])


class UIManager():
    def __init__(self):
        self.menu = {}

        self.selected_menu = "Build Shop"

        self.create_menu("Build Shop", 1050, 0)
        create_buttons(self.menu["Build Shop"])
        self.menu["Build Shop"].create_button("Small Troop", 10, 100)

    def create_menu(self, name, x, y, width=150, height=800, menu_col="black"):
        menu = Menu(x, y, name, width, height, menu_col)
        self.menu[name] = menu

    def loop(self, mouse_pos, coins=0):
        self.menu[self.selected_menu].loop(mouse_pos, coins)

    def draw(self):
        if self.selected_menu != "":
            self.menu[self.selected_menu].draw()
