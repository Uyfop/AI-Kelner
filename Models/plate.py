from enum import Enum


class PlateStatus(Enum):
    CLEAN = "Clean"
    DIRTY = "Dirty"


class Plate:
    def __init__(self):
        self.status = PlateStatus.CLEAN
