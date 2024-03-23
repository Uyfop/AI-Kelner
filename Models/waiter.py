from enum import Enum
import pygame


class WaiterStatus(Enum):
    IDLE = ("Idle",)
    BUSY = "Busy"


class Waiter:
    def __init__(self, img: pygame.Surface, x: int, y: int):
        self._img = img
        self.pos = {"x": x, "y": y}
        self.status = WaiterStatus.IDLE

    def change_status(self, new_status):
        if new_status in WaiterStatus:
            self.status = new_status

    def get_img(self):
        return self._img

    def get_pos(self):
        return self.pos

    def set_pos(self, x: int, y: int):
        self.pos = {"x": x, "y": y}

    def get_status(self):
        return self.status
