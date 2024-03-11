from enum import Enum
import os
import pygame
from dataclasses import dataclass
from typing import Any
from Models.waiter import Waiter

HEIGHT = 1000
WIDTH = 1000
CELL_COUNT = 10
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
        for row in range(0, HEIGHT, int(HEIGHT/grid.get_grid_size())):
            for col in range(0, WIDTH, int(WIDTH/grid.get_grid_size())):
                pygame.draw.rect(self.__surface, "brown", (row, col, WIDTH/grid.get_grid_size(), HEIGHT/grid.get_grid_size()), 1)

    def draw_objects(self, grid):
        grid = self.__grid.get_grid()
        grid[0][0].type = CellType.WAITER
        cell_size = HEIGHT // self.__grid.get_grid_size()

        for row in range(self.__grid.get_grid_size()):
            for col in range(self.__grid.get_grid_size()):
                cell = grid[row][col]
                if cell.type == CellType.WAITER:
                    waiter_image = pygame.image.load("Kelner-AI-LAB\\Assets\\Images\\kelner.jpg")  # Ładowanie obrazu kelnera
                    waiter_image = pygame.transform.scale(waiter_image, (cell_size, cell_size))  # Skalowanie obrazu do rozmiaru komórki
                    self.__surface.blit(waiter_image, (col * cell_size, row * cell_size))  # Rysowanie obrazu na ekranie

    def update_state(self): #zaimplementować
        pass

    def update_screen(self, grid):
        self.__surface.fill(COLOR)
        self.draw_grid(grid)
        self.draw_objects(grid)
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
