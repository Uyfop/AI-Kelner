from enum import Enum
import os
import random
import pygame
from dataclasses import dataclass
from typing import Any
from Models.waiter import Waiter
from Models.client import Client

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
        self.initialize_objects()

    def initialize_objects(self):
        waiter_img_path = os.path.join("Assets", "Images", "kelner.jpg")
        waiter_img = pygame.image.load(waiter_img_path)
        waiter_img = pygame.transform.scale(waiter_img, (HEIGHT // CELL_COUNT, HEIGHT // CELL_COUNT))
        waiter = Waiter(waiter_img, 0, 0)
        self.set_cell(0, 0, CellType.WAITER, waiter)

        client_folder_path = os.path.join("Assets", "Images", "clients")
        client_folder = client_folder_path
        client_images = [os.path.join(client_folder, filename) for filename in os.listdir(client_folder) if filename.endswith((".jpg"))]
        random_client_image_path = random.choice(client_images)

        client_img = pygame.image.load(random_client_image_path)
        client_img = pygame.transform.scale(client_img, (HEIGHT // CELL_COUNT, HEIGHT // CELL_COUNT))
        client = Client(client_img, 3, 3)
        self.set_cell(3, 3, CellType.CLIENT, client)

    def set_cell(self, row: int, col: int, cell_type: CellType, data: Any):
        self.__grid[row][col] = Cell(cell_type, data)

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
        cell_size = HEIGHT // self.__grid.get_grid_size()

        for row in range(self.__grid.get_grid_size()):
            for col in range(self.__grid.get_grid_size()):
                cell = grid[row][col]
                if cell.type == CellType.WAITER or cell.type == CellType.CLIENT:
                    image = cell.data._img
                    self.__surface.blit(image, (col * cell_size, row * cell_size))

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