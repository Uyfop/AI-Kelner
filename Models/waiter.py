import string
from enum import Enum


class WaiterStatus(Enum):
    IDLE = "Idle",
    BUSY = 'Busy'


class Waiter:
    def __init__(
            self,
            img: string,
            x: int,
            y: int
    ):
        self._img = img,
        self.pos = {'x': x, 'y': y}
        self.status = WaiterStatus.IDLE

    def change_status(self, new_status):
        if new_status in WaiterStatus:
            self.status = new_status
