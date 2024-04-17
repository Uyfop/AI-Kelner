from collections import deque
from Components import Cell, CellType
from Models import Client, Waiter, Table, Kitchen
from Models.direction import Direction


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

    def succ(self, current):
        successors = []
        x, y, direction = current

        if direction == Direction.NORTH and self._is_movable(x, y - 1):
            successors.append(((x, y - 1, direction), "forward"))
        if direction == Direction.SOUTH and self._is_movable(x, y + 1):
            successors.append(((x, y + 1, direction), "forward"))
        if direction == Direction.WEST and self._is_movable(x - 1, y):
            successors.append(((x - 1, y, direction), "forward"))
        if direction == Direction.EAST and self._is_movable(x + 1, y):
            successors.append(((x + 1, y, direction), "forward"))

        if direction == Direction.NORTH:
            successors.append(((x, y, Direction.NORTH.right), "right"))
        elif direction == Direction.EAST:
            successors.append(((x, y, Direction.EAST.right), "right"))
        elif direction == Direction.SOUTH:
            successors.append(((x, y, Direction.SOUTH.right), "right"))
        elif direction == Direction.WEST:
            successors.append(((x, y, Direction.WEST.right), "right"))

        if direction == Direction.NORTH:
            successors.append(((x, y, Direction.NORTH.left), "left"))
        elif direction == Direction.WEST:
            successors.append(((x, y, Direction.WEST.left), "left"))
        elif direction == Direction.SOUTH:
            successors.append(((x, y, Direction.SOUTH.left), "left"))
        elif direction == Direction.EAST:
            successors.append(((x, y, Direction.EAST.left), "left"))

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
                new_position = successor
                new_path = path + [(current, action)]
                queue.append((new_position, new_path))


        return None


    def _is_movable(self, x: int, y: int):
        if 0 <= x < self.__grid_size and 0 <= y < self.__grid_size:
            return self.__grid[x][y].type == CellType.EMPTY
        return False
    
    def move_waiter_forward(self, waiter: Waiter):
        x, y = waiter.get_pos()['x'], waiter.get_pos()['y']
        new_x, new_y = x, y
        
        if waiter.direction == Direction.NORTH:
            new_y = y - 1
        elif waiter.direction == Direction.SOUTH:
            new_y = y + 1
        elif waiter.direction == Direction.WEST:
            new_x = x - 1
        elif waiter.direction == Direction.EAST:
            new_x = x + 1

        waiter.set_pos(new_x, new_y)
