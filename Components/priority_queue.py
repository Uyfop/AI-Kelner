import heapq
from Models.node import Node

class PriorityQueue:
    def __init__(self) -> None:
        self.li: list[tuple[int, Node]] = []

    def heapify(self):
        heapq.heapify(self.li)

    def push(self, node: Node, weight: int) -> None:
        heapq.heappush(self.li, (weight, node))

    def pop(self) -> tuple[int, Node]:
        return heapq.heappop(self.li)