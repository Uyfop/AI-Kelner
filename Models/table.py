class Table:
    def __init__(self, x: int, y: int, number: int):
        self.x = x
        self.y = y
        self.number = number
        self.occupied = False

    def occupy(self):
        self.occupied = True

    def free(self):
        self.occupied = False

    def is_occupied(self):
        return self.occupied

    def get_number(self):
        return self.number

    def get_pos(self):
        return {"x": self.x, "y": self.y}

    def set_pos(self, x: int, y: int):
        self.x = x
        self.y = y