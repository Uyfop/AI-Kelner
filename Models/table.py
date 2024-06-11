import pygame

from Models.plate import Plate


class Table:
    def __init__(self, img: pygame.Surface, x: int, y: int, number: int, plate: Plate):
        self._img = img
        self.x = x
        self.y = y
        self.number = number
        self.occupied = False
        self.served = False
        self.plate = plate
        self.cost = 'inf'
        self.client = None

    def occupy(self, client):
        self.occupied = True
        self.client = client

    def free(self):
        self.occupied = False
        self.client = None

    def is_occupied(self):
        return self.client is not None

    def served(self):
        self.served = True

    def finished_eating(self):
        self.served = False

    def is_served(self):
        return self.served

    def get_number(self):
        return self.number

    def get_pos(self):
        return {"x": self.x, "y": self.y}

    def set_pos(self, x: int, y: int):
        self.x = x
        self.y = y

    def get_img(self):
        return self._img

    def get_cost(self):
        return self.cost

