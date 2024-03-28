from Models import Waiter, Client
from enum import Enum
from dataclasses import dataclass


class CellType(Enum):
    EMPTY = 0
    WALL = 1
    CLIENT = 2
    WAITER = 3
    TABLE = 4


@dataclass
class Cell:
    type: CellType
    data: None | Waiter | Client
