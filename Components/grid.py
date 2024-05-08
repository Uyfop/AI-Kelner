from collections import deque
from Components.priority_queue import PriorityQueue
from Components import Cell, CellType
from Models import Client, Waiter, Table, Kitchen
from Models.broken import Broken
from Models.water import Water
from Models.node import Node
from Models.banana import Banana


class Grid:
    def __init__(self, size: int):
        self.__grid_size = size
        self.__grid = [
            [Cell(CellType.EMPTY, None) for __ in range(size)] for __ in range(size)
        ]

    def set_cell(
            self, row: int, col: int, cell_type: CellType,
            data: None | Waiter | Client | Table | Kitchen | Water | Broken | Banana
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
            successors.append(((x + dx, y + dy, direction), "forward", self.cost((x + dx, y + dy))))

        successors.append(((x, y, direction.right), "right", 1))
        successors.append(((x, y, direction.left), "left", 1))

        return successors

    def bfs(self, start, goal):
        visited = set()
        queue = deque([Node(start)])

        while queue:
            elem = queue.popleft()

            if elem.state == goal:
                return self._build_path(elem)

            if elem.state in visited:
                continue

            visited.add(elem.state)

            for successor, action in self.succ(elem.state):
                queue.append(Node(successor, elem, action))

        return None

    def astar(self, start, goal):
        queue = PriorityQueue()
        queue.push(0, Node(start))
        visited = set()

        while queue:
            _, elem = queue.pop()

            if elem.state == goal:
                return self._build_path(elem)

            if elem.state not in visited:
                visited.add(elem.state)

                for successor, action, cost in self.succ(elem.state):
                    if cost == 'inf':
                        continue
                    g_value = cost
                    h_value = self.heuristic(elem.state, goal)
                    new_node = Node(successor, elem, action)

                    queue.push(g_value + h_value, new_node)

        return None

    def heuristic(self, node, goal):
        # Manhatan distance
        return abs(node[0] - goal[0]) + abs(node[1] - goal[1])

    def cost(self, position):
        x, y = position
        return self.get_cell(x, y).cost

    def _build_path(self, node):
        path = []
        while node:
            if node.action:
                path.append(node.action)
            node = node.parent
        return path[::-1]

    def _is_movable(self, x: int, y: int):
        return 0 <= x < self.__grid_size and 0 <= y < self.__grid_size

    def move_waiter_forward(self, waiter: Waiter):
        x, y = waiter.get_pos()['x'], waiter.get_pos()['y']
        dx, dy = waiter.direction.value
        new_x, new_y = x + dx, y + dy

        waiter.set_pos(new_x, new_y)
        self.set_cell(new_x, new_y, CellType.WAITER, waiter)
