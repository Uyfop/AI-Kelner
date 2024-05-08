import heapq
from Models.node import Node


class PriorityQueue:
    def __init__(self) -> None:
        self.li: list[tuple[int, Node]] = []

    def heapify(self):
        heapq.heapify(self.li)

    def push(self, priority: int, node: Node):
        heapq.heappush(self.li, (priority, node))

    def pop(self) -> tuple[int, Node]:
        return heapq.heappop(self.li)
