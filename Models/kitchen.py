from enum import Enum
import pygame


class KitchenStatus(Enum):
    COOKING = "Cooking"
    WAITING = "Waiting"

class Kitchen:

    def __init__(self, img: pygame.Surface,  x: int, y: int):
        self._img = img
        self.status = KitchenStatus.WAITING
        self.pos = {"x": x, "y": y}

    def set_pos(self, x: int, y: int):
        self.x = x
        self.y = y

    def get_status(self):
        return self.status

    def change_status(self, new_status: KitchenStatus):
        if new_status in KitchenStatus:
            self.status = new_status

    def get_img(self):
        return self._img