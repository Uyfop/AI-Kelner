import os
import random
import time

import pygame
import pandas as pd

from Components import Grid, CellType
from Models import Waiter, Client, Direction, Kitchen
from Models.plate import Plate
from Models.table import Table
from Models.water import Water
from Models.banana import Banana
from Components.decision_tree import DecisionTree
from Components.plate_classifier import PlateClassifier


class Simulation:
    def __init__(
            self,
            grid: Grid,
            surface: pygame.Surface,
            clock: pygame.time.Clock,
            fps: int,
            res: tuple[int, int],
            bg_color: tuple[int, int, int],
            wall_color: tuple[int, int, int],
            move_delay: int = 1,
            decision_tree: DecisionTree = None,
            plate_classifier: PlateClassifier = None,
            meal_mapping: dict = None
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
        self.waters = []
        self.served_clients = []
        self.next_move = pygame.time.get_ticks()
        self.move_delay = move_delay
        self.decision_tree = decision_tree
        self.meal_mapping = meal_mapping
        self.plate_classifier = plate_classifier
        self.initialize_objects()

    def initialize_objects(self):
        grid_size = self.__grid.get_grid_size()

        waiter_img_path = os.path.join("Assets", "Images", "waiter.png")
        waiter_img = pygame.image.load(waiter_img_path)
        waiter_img = pygame.transform.scale(
            waiter_img,
            (self.window_width // grid_size, self.window_height // grid_size),
        )
        waiter = Waiter(waiter_img, 1, 1, Direction.NORTH, self.__grid)
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

        water_img_path = os.path.join("Assets", "Images", "water.png")
        water_img = pygame.image.load(water_img_path)
        water_img = pygame.transform.scale(
            water_img,
            (self.window_width // grid_size, self.window_height // grid_size),
        )
        water = Water(water_img, 10, 4)
        self.waters.append(water)
        self.__grid.set_cell(10, 4, CellType.WATER, water)

        water = Water(water_img, 17, 17)
        self.waters.append(water)
        self.__grid.set_cell(17, 17, CellType.WATER, water)

        water = Water(water_img, 0, 10)
        self.waters.append(water)
        self.__grid.set_cell(0, 10, CellType.WATER, water)

        water = Water(water_img, 0, 1)
        self.waters.append(water)
        self.__grid.set_cell(0, 1, CellType.WATER, water)

        water = Water(water_img, 0, 2)
        self.waters.append(water)
        self.__grid.set_cell(0, 2, CellType.WATER, water)

        water = Water(water_img, 0, 3)
        self.waters.append(water)
        self.__grid.set_cell(0, 3, CellType.WATER, water)

        water = Water(water_img, 1, 3)
        self.waters.append(water)
        self.__grid.set_cell(1, 3, CellType.WATER, water)

        water = Water(water_img, 3, 1)
        self.waters.append(water)
        self.__grid.set_cell(3, 1, CellType.WATER, water)

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
        current_position = (self.waiter.pos['x'], self.waiter.pos['y'], self.waiter.direction)
        if len(self.get_empty_tables()) != 0:
            table = random.choice(self.get_empty_tables())
            self.spawn_client(table.x, table.y, table)
        else:
            pass

        self.spawn_banana()

        occupied_tables = [table for table in self.tables if table.is_occupied()]
        if occupied_tables:
            target_table = random.choice(occupied_tables)
            available_positions = self.get_available_positions(target_table)
            if available_positions:
                return self.get_shortest_path(current_position, available_positions, target_table)

    def get_meal_suggestion(self, target_table: Table):
        client: Client = target_table.client

        # parse client data into pandas dataframe for tree decision
        data = {
            "age": [client.age],
            "budget": [client.budget],
            "is_female": [1 if client.is_female else 0],
            "is_vegetarian": [1 if client.is_vegetarian else 0],
            "is_lactose_intolerant": [1 if client.is_lactose_intolerant else 0],
            "is_alcohol_abstinent": [1 if client.is_alcohol_abstinent else 0],
            "is_fit": [1 if client.is_fit else 0]
        }

        continents = {
            "africa": "continent_africa",
            "asia": "continent_asia",
            "europe": "continent_europe",
            "north_america": "continent_north_america",
            "oceania": "continent_oceania",
            "south_america": "continent_south_america",
        }

        data.update({continents.get(client.continent): 1})

        for i in continents.items():
            if i not in data.keys():
                data.update({i[1]: 0})

        df = pd.DataFrame(data)
        desired_order = [
            "age",
            "budget",
            "is_female",
            "is_vegetarian",
            "is_lactose_intolerant",
            "is_alcohol_abstinent",
            "is_fit",
            "continent_africa",
            "continent_asia",
            "continent_europe",
            "continent_north_america",
            "continent_oceania",
            "continent_south_america",
        ]

        df = df.reindex(columns=desired_order)
        suggestion = self.decision_tree.predict(df)
        print(target_table.client)
        if not target_table.client.plate:
            print(f"suggested meal: {self.meal_mapping[suggestion[0]]}")
            target_table.client.plate = self._get_plate_path("./neural_network_training/full")
            self._roll_plate_change()
            self.served_clients.append(target_table.client)
        else:
            prediciton = self.plate_classifier.predict(target_table.client.plate)
            if prediciton > 0.5: 
                print("client's plate is not empty yet, continue")
            else:
                print("client's plate is empty, take it")
                target_table.client.plate = None
                self.served_clients.remove(target_table.client)
            self._roll_plate_change(target_table.client)
        

    def _roll_plate_change(self, client_to_omit=None):
        for client in self.served_clients:
            if client_to_omit and client_to_omit == client:
                continue
            switch_to_empty= random.choices([True, False], weights=[0.20,0.80])[0]
            if switch_to_empty: 
                client.plate = self._get_plate_path("./neural_network_training/empty")

    def _get_plate_path(self, directory: str) -> str:
        plate_img_path = random.choice(os.listdir(directory))
        return f"{directory}/{plate_img_path}"

    def get_available_positions(self, table):
        x, y = table.x, table.y
        directions = [(0, -1, Direction.EAST), (0, 1, Direction.WEST)]
        
        available_positions = []
        for dx, dy, direction in directions:
            new_x, new_y = x + dx, y + dy
            if self.__grid.get_cell(new_x, new_y).type == CellType.EMPTY:
                available_positions.append((new_x, new_y, direction))
        
        return available_positions

    
    def get_shortest_path(self, current_position, available_positions, target_table):
        paths = [
            (self.__grid.astar(current_position, (x, y, direction)), (x, y, direction))
            for x, y, direction in available_positions
        ]

        shortest_path, target_position = min(paths, key=lambda x: len(x[0]))
        # print(f"target: {target_position[0]} {target_position[1]}")
        # print(f"actions: {[action for action in shortest_path]}")
        self.move_waiter(shortest_path, target_table)

    def move_waiter(self, path, target_table):
        while path:
            current_time = pygame.time.get_ticks()
            if current_time <= self.next_move:
                continue
            action = path.pop(0)
            self.update_screen()
            pygame.time.delay(300)
            if action == "forward":
                x, y = self.waiter.get_pos()['x'], self.waiter.get_pos()['y']
                self.__grid.set_cell(x, y, CellType.EMPTY, None)
                self.waiter.try_move_forward()
            elif action == "right":
                self.waiter.rotate_right()
            elif action == "left":
                self.waiter.rotate_left()
            self.next_move = current_time + self.move_delay
        self.get_meal_suggestion(target_table)

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
        continents = [
            "europe",
            "asia",
            "north_america",
            "south_america",
            "africa",
            "oceania"
        ]
        continent = random.choice(continents)
        age = random.randint(18, 70)
        budget = random.choice([0, 1, 2])

        is_female = random.choices([True, False])

        def random_bool():
            return random.choices([True, False])[0]

        is_vegetarian = random_bool()
        is_lactose_intolerant = random_bool()
        is_alcohol_abstinent = random_bool()
        is_fit = random_bool()

        client = Client(
            client_img,
            x - 1,
            y,
            age,
            continent,
            budget,
            is_female,
            is_vegetarian,
            is_lactose_intolerant,
            is_alcohol_abstinent,
            is_fit
        )
        self.clients.append(client)
        self.__grid.set_cell(x - 1, y, CellType.CLIENT, client)
        table.occupy(client) 

    def update_screen(self):
        self.__surface.fill(self.background_color)
        self.draw_grid()
        self.draw_objects()
        pygame.display.flip()

    def update(self):
        self.update_state()
        self.despawn_bananas()
        self.update_screen()

    def spawn_banana(self):
        grid_size = self.__grid.get_grid_size()
        banana_img_path = os.path.join("Assets", "Images", "banana.png")
        banana_img = pygame.image.load(banana_img_path)
        banana_img = pygame.transform.scale(
            banana_img,
            (self.window_width // grid_size, self.window_height // grid_size),
        )

        empty_squares = []
        bananas_on_grid = 0
        for x in range(grid_size):
            for y in range(grid_size):
                if x + 1 < 20 and self.__grid.get_cell(x + 1, y).type == CellType.TABLE:
                    continue
                if self.__grid.get_cell(x, y).type == CellType.EMPTY:
                    empty_squares.append((x, y))
                elif self.__grid.get_cell(x, y).type == CellType.BANANA:
                    bananas_on_grid += 1

        for _ in range(40 - bananas_on_grid):
            x, y = random.choice(empty_squares)
            banana = Banana(banana_img, x, y)

            self.__grid.set_cell(x, y, CellType.BANANA, banana)
            empty_squares.remove((x, y))

    def despawn_bananas(self):
        current_time = time.time()
        despawn_time = 20

        for x in range(self.__grid.get_grid_size()):
            for y in range(self.__grid.get_grid_size()):
                cell = self.__grid.get_cell(x, y)
                if cell.type == CellType.BANANA:
                    banana = cell.data
                    if current_time - banana.timestamp >= despawn_time:
                        self.__grid.set_cell(x, y, CellType.EMPTY, None)
