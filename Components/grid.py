from collections import deque
from Components import Cell, CellType
from Models import Client, Waiter, Table, Kitchen
from Models.broken import Broken
from Models.direction import Direction
from Models.water import Water


class Grid:
    def __init__(self, size: int):
        self.__grid_size = size
        self.__grid = [
            [Cell(CellType.EMPTY, None) for __ in range(size)] for __ in range(size)
        ]

    def set_cell(
        self, row: int, col: int, cell_type: CellType, data: None | Waiter | Client | Table | Kitchen | Water | Broken
    ):
        self.__grid[row][col] = Cell(cell_type, data)

    def get_cell(self, row: int, col: int) -> Cell:
        return self.__grid[row][col]

    def get_grid(self) -> list[Cell]:
        return self.__grid

    def get_grid_size(self) -> int:
        return self.__grid_size


    def succ(self, current):
        successors = []
        x, y, direction = current

        dx, dy = direction.value

        if self._is_movable(x + dx, y + dy):
            successors.append(((x + dx, y + dy, direction), "forward"))

        successors.append(((x, y, direction.right), "right"))
        successors.append(((x, y, direction.left), "left"))


        return successors

    def bfs(self, start, goal):
        visited = set()
        queue = deque([(start, [])])

        while queue:
            current, path = queue.popleft()
            if current == goal:
                return path

            if current in visited:
                continue

            visited.add(current)

            for successor, action in self.succ(current):
                new_path = path + [action]
                queue.append((successor, new_path))

        return None


    def _is_movable(self, x: int, y: int):
        if 0 <= x < self.__grid_size and 0 <= y < self.__grid_size:
            return self.__grid[x][y].type == CellType.EMPTY
        return False
    def move_waiter_forward(self, waiter: Waiter):
        x, y = waiter.get_pos()['x'], waiter.get_pos()['y']
        dx, dy = waiter.direction.value
        new_x, new_y = x + dx, y + dy

        waiter.set_pos(new_x, new_y)
        self.set_cell(new_x, new_y, CellType.WAITER, waiter)
