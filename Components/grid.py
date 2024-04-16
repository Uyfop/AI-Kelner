from Components import Cell, CellType
from Models import Client, Waiter, Table, Kitchen


class Grid:
    def __init__(self, size: int):
        self.__grid_size = size
        self.__grid = [
            [Cell(CellType.EMPTY, None) for __ in range(size)] for __ in range(size)
        ]

    def set_cell(
        self, row: int, col: int, cell_type: CellType, data: None | Waiter | Client | Table | Kitchen
    ):
        self.__grid[row][col] = Cell(cell_type, data)

    def get_cell(self, row: int, col: int) -> Cell:
        return self.__grid[row][col]

    def get_grid(self) -> list[Cell]:
        return self.__grid

    def get_grid_size(self) -> int:
        return self.__grid_size

    def bfs(self, start, goal):
        # bfs state search, keep track of the direction when looking at moves
        ...

    def _is_movable(self, x: int, y: int):
        ...
    
    def move_waiter_forward(self, waiter: Waiter):
        # use waiter.direction
        ...
