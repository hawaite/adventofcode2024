from dataclasses import dataclass
from enum import Enum

@dataclass(frozen=True)
class Point:
    col: int
    row: int

class Direction(Enum):
    NORTH = Point(0,-1)
    NORTHEAST = Point(1,-1)
    EAST = Point(1,0)
    SOUTHEAST = Point(1,1)
    SOUTH = Point(0,1)
    SOUTHWEST = Point(-1, 1)
    WEST = Point(-1, 0)

    def get_rotate_ninty_cw(self):
        if self.name == "NORTH":
            return Direction.EAST
        if self.name == "EAST":
            return Direction.SOUTH
        if self.name == "SOUTH":
            return Direction.WEST
        if self.name == "WEST":
            return Direction.NORTH
        
    def get_rotate_ninty_ccw(self):
        if self.name == "NORTH":
            return Direction.WEST
        if self.name == "WEST":
            return Direction.SOUTH
        if self.name == "SOUTH":
            return Direction.EAST
        if self.name == "EAST":
            return Direction.NORTH

@dataclass
class DirectionalPoint:
    point: Point
    direction: Direction
    
class Grid:
    # assumes a list of lists of all the same length
    def __init__(self, lines):
        self.width = len(lines[0])
        self.height = len(lines)
        self.grid = []

        # explode the string in to mutable list of lists
        if isinstance(lines[0], str): # if its a string, split it
            for line in lines:
                self.grid.append([x for x in line])
        else:
            for line in lines:
                self.grid.append(line.copy())

    def get_value(self, location:Point):
        return self.grid[location.row][location.col]
    
    def set_value(self, location:Point, value):
        self.grid[location.row][location.col] = value

    def position_in_bounds(self, location:Point):
        return ( location.col >= 0 and location.row >= 0 and location.col < self.width and location.row < self.height )