from enum import Enum
import pygame
from dataclasses import dataclass
from typing import Any
from Models import client
from Models import waiter


HEIGHT = 400
WIDTH = 400
CELL_COUNT = 10
FPS = 60

## TODO: 
# - obiekty kelner, klient
# - zaimplementować rysowanie siatki 
# - zaimplementować rysowanie obiektów
# - przenieść implementacje obiektów do osobnych plików (potem)

class CellType(Enum):
    EMPTY = 0
    WALL = 1
    CLIENT = 2
    WAITER = 3


@dataclass
class Cell:
    type: CellType
    data: Any  # do zmiany jak juz wprowadzimy obiekty kelner klient etc


class Grid:
    def __init__(self, size: int):
        self.__grid_size = size
        self.__grid = [
            [Cell(None, None) for __ in range(self.__grid_size)] # po implementacji obiektów ustawić type i data
            for __ in range(self.__grid_size)
        ]

    def get_grid(self) -> list[Cell]:
        return self.__grid

    def get_grid_size(self) -> int:
        return self.__grid_size


class Simulation:
    def __init__(
        self,
        grid: Grid,
        surface: pygame.Surface,
        clock: pygame.time.Clock,
        fps: int,
        res: tuple[int, int],
    ):
        self.__res = res
        self.__grid = grid
        self.__surface = surface
        self.clock = clock
        self.fps = fps

    def draw_grid(self): #zaimplementować
        pygame.draw.line(self.__surface, "black", (0, 0), self.__res) 

    def draw_objects(self): #zaimplementować
        pass

    def update_state(self): #zaimplementować
        pass

    def update_screen(self):
        self.__surface.fill("white")
        self.draw_grid()
        self.draw_objects()
        pygame.display.flip()

    def update(self):
        self.update_state()
        self.update_screen()


def main():
    running = True
    pygame.init()
    res = (HEIGHT, WIDTH)

    surface = pygame.display.set_mode(res)
    clock = pygame.time.Clock()
    grid = Grid(CELL_COUNT)

    sim = Simulation(grid, surface, clock, FPS, (HEIGHT, WIDTH))

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        sim.update()
        sim.clock.tick(sim.fps)


if __name__ == "__main__":
    main()
