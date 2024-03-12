from enum import Enum
import pygame


class ClientStatus(Enum):
    WAITING = "Waiting"
    ORDERING = "Ordering"
    SERVED = "Served"


class Client:
    def __init__(
            self,
            img: pygame.Surface,
            x: int,
            y: int
    ):
        self._img = img
        self.pos = {'x': x, 'y': y}
        self.status = ClientStatus.WAITING

    def change_status(self, new_status):
        if new_status in ClientStatus:
            self.status = new_status
