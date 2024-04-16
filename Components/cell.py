from Models import Waiter, Client, Kitchen, Table
from enum import Enum
from dataclasses import dataclass


class CellType(Enum):
    EMPTY = 0
    WALL = 1
    CLIENT = 2
    WAITER = 3
    TABLE = 4
    KITCHEN = 5


@dataclass
class Cell:
    type: CellType
    data: None | Waiter | Client | Table | Kitchen
