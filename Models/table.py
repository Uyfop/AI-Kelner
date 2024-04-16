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

    def occupy(self):
        self.occupied = True

    def free(self):
        self.occupied = False

    def is_occupied(self):
        return self.occupied
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
