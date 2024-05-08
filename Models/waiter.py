from enum import Enum
import pygame
from typing import Any
from .direction import Direction


class WaiterStatus(Enum):
    IDLE = "Idle"
    BUSY = "Busy"


class Waiter:
    def __init__(self, img: pygame.Surface, x: int, y: int, direction, grid: Any):
        self._img = img
        self.pos = {"x": x, "y": y}
        self.status = WaiterStatus.IDLE
        self.direction = direction
        self.grid = grid
        self.cost = 'inf'

    def rotate_left(self):
        self.direction = self.direction.left

    def rotate_right(self):
        self.direction = self.direction.right

    def try_move_forward(self):
        self.grid.move_waiter_forward(self)

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

    def rotate_image(self):
        angle = 0
        if self.direction == Direction.NORTH:
            angle = 0
        elif self.direction == Direction.EAST:
            angle = 270
        elif self.direction == Direction.SOUTH:
            angle = 180
        elif self.direction == Direction.WEST:
            angle = 90

        rotated_image = pygame.transform.rotate(self._img, angle)
        return rotated_image

    def get_cost(self):
        return self.cost