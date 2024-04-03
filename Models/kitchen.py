from enum import Enum


class KitchenStatus(Enum):
    COOKING = "Cooking"
    WAITING = "Waiting"

class Kitchen:

    def __init__(self, x: int, y: int):
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

