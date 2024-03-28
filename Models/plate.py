from enum import Enum


class PlateStatus(Enum):
    CLEAN = "Clean"
    MEAL = "Meal"
    DIRTY = "Dirty"


class Plate:
    def __init__(self):
        self.status = PlateStatus.CLEAN

    def change_status(self, new_status: PlateStatus):
        if new_status in PlateStatus:
            self.status = new_status

    def get_status(self):
        return self.status

