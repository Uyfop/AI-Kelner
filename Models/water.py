from typing import Any

import pygame


class Water:
    def __init__(self, img: pygame.Surface, x: int, y: int):
        self._img = img
        self.pos = {"x": x, "y": y}
        self.cost = 10

    def set_pos(self, x: int, y: int):
        self.x = x
        self.y = y


    def get_img(self):
        return self._img

    def get_cost(self):
        return self.cost