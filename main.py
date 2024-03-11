from enum import Enum
import pygame
from dataclasses import dataclass
from typing import Any

HEIGHT = 400
WIDTH = 400
CELL_COUNT = 5
FPS = 60
COLOR = (218, 198, 169)

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

    def draw_grid(self, grid):
        for i in range(int(WIDTH/grid.get_grid_size()), WIDTH, int(WIDTH/grid.get_grid_size())):
            pygame.draw.line(self.__surface, "black", (0, i), (WIDTH, i))
        for i in range(int(HEIGHT/grid.get_grid_size()), HEIGHT, int(HEIGHT/grid.get_grid_size())):
            pygame.draw.line(self.__surface, "black", (i, 0), (i, HEIGHT))

    def draw_objects(self): #zaimplementować
        pass

    def update_state(self): #zaimplementować
        pass

    def update_screen(self, grid):
        self.__surface.fill(COLOR)
        self.draw_grid(grid)
        self.draw_objects()
        pygame.display.flip()

    def update(self, grid):
        self.update_state()
        self.update_screen(grid)


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
        sim.update(grid)
        sim.clock.tick(sim.fps)


if __name__ == "__main__":
    main()
