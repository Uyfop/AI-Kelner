import os
import random
import time
import pygame

from Components import Grid, CellType
from Models import Waiter, Client, Direction, Kitchen
from Models.plate import Plate
from Models.table import Table


class Simulation:
    def __init__(
            self,
            grid: Grid,
            surface: pygame.Surface,
            clock: pygame.time.Clock,
            fps: int,
            res: tuple[int, int],
            bg_color: tuple[int, int, int],
            wall_color: tuple[int, int, int]
    ):
        self.window_width, self.window_height = res[0], res[1]
        self.__grid = grid
        self.__surface = surface
        self.clock = clock
        self.fps = fps
        self.background_color = bg_color
        self.wall_color = wall_color
        self.waiter = None
        self.kitchen = None
        self.clients = []
        self.tables = []
        self.last_client_spawn_time = time.time()
        self.initialize_objects()

    def initialize_objects(self):
        grid_size = self.__grid.get_grid_size()

        waiter_img_path = os.path.join("Assets", "Images", "waiter.png")
        waiter_img = pygame.image.load(waiter_img_path)
        waiter_img = pygame.transform.scale(
            waiter_img,
            (self.window_width // grid_size, self.window_height // grid_size),
        )
        waiter = Waiter(waiter_img, 1, 1, Direction.EAST, self.__grid)
        self.waiter = waiter

        self.__grid.set_cell(self.waiter.pos['x'], self.waiter.pos['y'], CellType.WAITER, waiter)

        kitchen_img_path = os.path.join("Assets", "Images", "kitchen.png")
        kitchen_img = pygame.image.load(kitchen_img_path)
        kitchen_img = pygame.transform.scale(
            kitchen_img,
            (self.window_width // grid_size, self.window_height // grid_size),
        )
        self.kitchen = Kitchen(kitchen_img, 0, 0)
        self.__grid.set_cell(self.kitchen.pos['x'], self.kitchen.pos['y'], CellType.KITCHEN, self.kitchen)

        table_img_path = os.path.join("Assets", "Images", "table.png")
        table_img = pygame.image.load(table_img_path)
        table_img = pygame.transform.scale(
            table_img,
            (self.window_width // grid_size, self.window_height // grid_size),
        )
        x = 0
        for i in range(2, grid_size, 4):
            for j in range(2, grid_size, 4):
                x += 1
                plate = Plate()
                table = Table(table_img, i, j, x, plate)
                self.tables.append(table)
                self.__grid.set_cell(i, j, CellType.TABLE, table)

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
                if cell.type != CellType.EMPTY:
                    if isinstance(cell.data, Waiter):
                        waiter = cell.data
                        rotated_image = waiter.rotate_image()
                        self.__surface.blit(rotated_image, (column_idx * cell_size, row_idx * cell_size))
                    else:
                        image = cell.data.get_img()
                        self.__surface.blit(image, (column_idx * cell_size, row_idx * cell_size))

    def update_state(self):
        grid_size = self.__grid.get_grid_size()
        current_position = (self.waiter.pos['x'], self.waiter.pos['y'])
        available_positions = []

        for x in range(grid_size):
            for y in range(grid_size):
                if self.__grid.get_cell(x, y).type == CellType.EMPTY:
                    available_positions.append((x, y))

        if available_positions:
            target_position = random.choice(available_positions)
            direction = (target_position[0] - current_position[0], target_position[1] - current_position[1])

            self.move_waiter(direction)


        current_time = time.time()
        if current_time - self.last_client_spawn_time >= 5:  # spawn kolejnego klienta po 5 sekundach
            if len(self.get_empty_tables()) != 0:
                table = random.choice(self.get_empty_tables())
                self.spawn_client(table.x, table.y, table)
                self.last_client_spawn_time = current_time
            else:
                pass

    def get_empty_tables(self):
        empty_tables = []
        grid_size = self.__grid.get_grid_size()
        tables = self.tables
        for x in range(grid_size):
            for y in range(grid_size):
                if self.__grid.get_cell(x, y).type == CellType.TABLE:
                    for table in tables:
                        if not table.is_occupied():
                            empty_tables.append(table)

        return empty_tables

    def spawn_client(self, x, y, table):
        client_folder_path = os.path.join("Assets", "Images", "clients")
        client_folder = client_folder_path
        client_images = [
            os.path.join(client_folder, filename)
            for filename in os.listdir(client_folder)
            if filename.endswith(".png")
        ]
        random_client_image_path = random.choice(client_images)
        client_img_path = random_client_image_path  # wybierz losowy obraz klienta
        client_img = pygame.image.load(client_img_path)
        client_img = pygame.transform.scale(
            client_img,
            (self.window_width // self.__grid.get_grid_size(), self.window_height // self.__grid.get_grid_size()),
        )

        client = Client(client_img, x - 1, y)
        self.clients.append(client)
        self.__grid.set_cell(x - 1, y, CellType.CLIENT, client)
        table.occupy()

    def move_waiter(self, direction):
        current_x = self.waiter.pos['x']
        current_y = self.waiter.pos['y']

        target_x = current_x + direction[0]
        target_y = current_y + direction[1]

        self.__grid.set_cell(current_x, current_y, CellType.EMPTY, None)

        steps = max(abs(target_x - current_x), abs(target_y - current_y))

        for _ in range(steps):
            current_x += direction[0] / steps
            current_y += direction[1] / steps

            int_x = int(round(current_x))
            int_y = int(round(current_y))

            if self.__grid.get_cell(int_x, int_y).type != CellType.EMPTY:
                current_x = self.waiter.pos['x']
                current_y = self.waiter.pos['y']
                self.__grid.set_cell(current_x, current_y, CellType.WAITER, self.waiter)
                return

            self.waiter.pos['x'] = int_x
            self.waiter.pos['y'] = int_y
            self.__grid.set_cell(int_x, int_y, CellType.WAITER, self.waiter)

            self.update_screen()
            pygame.time.delay(100)
            self.__grid.set_cell(int_x, int_y, CellType.EMPTY, None)

        self.waiter.pos['x'] = target_x
        self.waiter.pos['y'] = target_y

        self.__grid.set_cell(target_x, target_y, CellType.WAITER, self.waiter)
        pygame.time.delay(1000)

    def update_screen(self):
        self.__surface.fill(self.background_color)
        self.draw_grid()
        self.draw_objects()
        pygame.display.flip()

    def update(self):
        self.update_state()
        self.update_screen()
