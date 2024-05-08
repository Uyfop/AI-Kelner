import pygame
import time


class Banana:
    def __init__(self, img: pygame.Surface, x: int, y: int):
        self._img = img
        self.pos = {"x": x, "y": y}
        self.timestamp = time.time()

    def set_pos(self, x: int, y: int):
        self.x = x
        self.y = y

    def get_img(self):
        return self._img
