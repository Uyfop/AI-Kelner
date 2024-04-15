from enum import Enum

class Direction(Enum):
    NORTH = (0, -1)
    EAST = (1, 0)
    SOUTH = (-1, 0)
    WEST = (0, -1)

Direction.NORTH.left = Direction.WEST
Direction.NORTH.right = Direction.EAST
Direction.EAST.left = Direction.NORTH
Direction.EAST.right = Direction.SOUTH
Direction.SOUTH.left = Direction.EAST
Direction.SOUTH.right = Direction.WEST
Direction.WEST.left = Direction.SOUTH
Direction.WEST.right = Direction.NORTH