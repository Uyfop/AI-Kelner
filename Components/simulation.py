import os
import random
import pygame

from Components import Grid, CellType
from Models import Waiter, Client


class Simulation:
    def __init__(
        self,
        grid: Grid,
        surface: pygame.Surface,
        clock: pygame.time.Clock,
        fps: int,
        res: tuple[int, int],
        bg_color: tuple[int, int, int],
        wall_color = tuple[int, int, int]
    ):
        self.window_width, self.window_height = res[0], res[1]
        self.__grid = grid
        self.__surface = surface
        self.clock = clock
        self.fps = fps
        self.background_color = bg_color
        self.wall_color = wall_color
        self.initialize_objects()

    def initialize_objects(self):
        grid_size = self.__grid.get_grid_size()

        waiter_img_path = os.path.join("Assets", "Images", "waiter.png")
        waiter_img = pygame.image.load(waiter_img_path)
        waiter_img = pygame.transform.scale(
            waiter_img,
            (self.window_width // grid_size, self.window_height // grid_size),
        )
        waiter = Waiter(waiter_img, 0, 0)
        self.__grid.set_cell(0, 0, CellType.WAITER, waiter)

        client_folder_path = os.path.join("Assets", "Images", "clients")
        client_folder = client_folder_path
        client_images = [
            os.path.join(client_folder, filename)
            for filename in os.listdir(client_folder)
            if filename.endswith((".png"))
        ]
        random_client_image_path = random.choice(client_images)

        client_img = pygame.image.load(random_client_image_path)
        client_img = pygame.transform.scale(
            client_img,
            (self.window_width // grid_size, self.window_height // grid_size),
        )
        client = Client(client_img, 3, 3)
        self.__grid.set_cell(3, 3, CellType.CLIENT, client)
        self.__grid.set_cell(4,4, CellType.WALL, None)

    def draw_grid(self):
        grid_size = self.__grid.get_grid_size()
        for row in range(0, self.window_height, self.window_height // grid_size):
            for col in range(0, self.window_width, self.window_width // grid_size):
                pygame.draw.rect(
                    self.__surface,
                    self.wall_color,
                    (
                        row,
                        col,
                        self.window_width // grid_size,
                        self.window_height // grid_size,
                    ),
                    1,
                )

    def draw_objects(self):
        grid = self.__grid.get_grid()
        grid_size = self.__grid.get_grid_size()
        cell_size = self.window_height // grid_size

        for row_idx, row in enumerate(grid):
            for column_idx, cell in enumerate(row):
                if cell.type == CellType.WAITER or cell.type == CellType.CLIENT:
                    image = cell.data._img
                    self.__surface.blit(
                        image, (column_idx * cell_size, row_idx * cell_size)
                    )
                elif cell.type == CellType.WALL:
                    wall_rect = pygame.Rect(column_idx * cell_size, row_idx * cell_size, cell_size, cell_size)
                    pygame.draw.rect(self.__surface, self.wall_color, wall_rect) 

    def update_state(self):  # zaimplementować
        pass

    def update_screen(self):
        self.__surface.fill(self.background_color)
        self.draw_grid()
        self.draw_objects()
        pygame.display.flip()

    def update(self):
        self.update_state()
        self.update_screen()
