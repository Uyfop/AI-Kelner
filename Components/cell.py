from Models import Waiter, Client, Kitchen, Table
from enum import Enum
from dataclasses import dataclass, field

from Models.broken import Broken
from Models.water import Water


class CellType(Enum):
    EMPTY = 0
    WALL = 1
    CLIENT = 2
    WAITER = 3
    TABLE = 4
    KITCHEN = 5
    WATER = 6
    BROKEN = 7




@dataclass
class Cell:
    type: CellType
    data: None | Waiter | Client | Table | Kitchen | Water | Broken
    cost: int = field(default=1, init=False)

    def __post_init__(self):
        if self.type == CellType.WATER:
            self.cost = 100
        elif self.type == CellType.BROKEN:
            self.cost = 10
        else:
            self.cost = 1