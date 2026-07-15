import pygame

import Data.constants as constants

from UI.buttons import Buttons


class Menu():
    def __init__(self, x, y, width=150, height=800, menu_col="#2C313C"):
        self.rect = pygame.Rect(x, y, width, height)
        self.menu_col = menu_col

        self.buttons = []
        self.no_buttons = 0

        self.current_function = False

    def create_button(self, text, function, button_col, text_col, price):
        self.no_buttons += 1

        center_x = self.rect.centerx
        center_y = (60 * self.no_buttons) + 20

        button = Buttons(text, function, button_col,
                         text_col, (center_x, center_y), price)

        self.buttons.append(button)

    def loop(self, mouse_pos, coins):
        for button in self.buttons:
            button.mouse_detection(mouse_pos, coins)

    def get_function(self, mouse_pos):
        clicked_button = False
        for button in self.buttons:
            if button.rect.collidepoint(mouse_pos):
                self.current_function = button.get_function()
                clicked_button = True
                break

        return self.current_function, clicked_button

    def draw(self):
        pygame.draw.rect(constants.WIN, self.menu_col, self.rect)
        for button in self.buttons:
            button.draw()
