from enum import Enum
import pygame


class ClientStatus(Enum):
    WAITING = "Waiting"
    ORDERING = "Ordering"
    SERVED = "Served"
    EATING = "Eating"


class Client:
    def __init__(self, img: pygame.Surface, x: int, y: int):
        self._img = img
        self.pos = {"x": x, "y": y}
        self.status = ClientStatus.WAITING

    def change_status(self, new_status: ClientStatus):
        if new_status in ClientStatus:
            self.status = new_status

    def get_img(self):
        return self._img

    def get_pos(self):
        return self.pos

    def set_pos(self, x: int, y: int):
        self.pos = {"x": x, "y": y}

    def get_status(self):
        return self.status
