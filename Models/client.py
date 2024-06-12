from enum import Enum
import pygame


class ClientStatus(Enum):
    WAITING = "Waiting"
    ORDERING = "Ordering"
    SERVED = "Served"
    EATING = "Eating"


class Client:
    def __init__(self, img: pygame.Surface, x: int, y: int, age: int, continent: str, budget: int,
                 is_female: bool, is_vegetarian: bool, is_lactose_intolerant: bool,
                 is_alcohol_abstinent: bool, is_fit: bool):
        self._img = img
        self.pos = {"x": x, "y": y}
        self.status = ClientStatus.WAITING
        self.cost = 'inf'

        self.age = age
        self.continent = continent
        self.budget = budget
        self.is_female = is_female
        self.is_vegetarian = is_vegetarian
        self.is_lactose_intolerant = is_lactose_intolerant
        self.is_alcohol_abstinent = is_alcohol_abstinent
        self.is_fit = is_fit

    def __str__(self) -> str:
        return f"Client(age: {self.age}, continent: {self.continent}, budget: {self.budget}," +\
            f" is_female: {self.is_female}, is_vegetarian: {self.is_vegetarian}, is_lactose_intolerant: {self.is_lactose_intolerant}," +\
                f" is_alcohol_abstinent: {self.is_alcohol_abstinent}, is_fit: {self.is_fit})"

    def change_status(self, new_status: ClientStatus):
        if new_status in ClientStatus:
            self.status = new_status

    def get_img(self):
        return self._img

    def get_pos(self):
        return self.pos

    def set_pos(self, x: int, y: int):
        self.pos = {"x": x, "y": y}

    def get_status(self):
        return self.status

    def get_cost(self):
        return self.cost

    def get_age(self):
        return self.age

    def get_continent(self):
        return self.continent

    def get_budget(self):
        return self.budget

    def get_is_female(self):
        return self.is_female

    def get_is_vegetarian(self):
        return self.is_vegetarian

    def get_is_lactose_intolerant(self):
        return self.is_lactose_intolerant

    def get_is_alcohol_abstinent(self):
        return self.is_alcohol_abstinent

    def get_is_fit(self):
        return self.is_fit
