from dataclasses import dataclass
from enum import Enum
from typing import Callable

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
    NORTHWEST = Point(-1, -1)

    # returns a new enum instance value rotated closwise by degrees.
    # only values divisible by 45 are valid
    # can be negative for counter clockwise
    def rotate(self, degrees:int):
        ordering = list(Direction)
        (places, remainder) = divmod(degrees, 45)
        if remainder != 0:
            raise ValueError("degrees must be divisible by 45")
        ix = ordering.index(self)
        ix += places
        ix = ix % len(ordering)
        return ordering[ix]

cardinal_directions = [Direction.NORTH, Direction.EAST, Direction.SOUTH, Direction.WEST ]
ordinal_directions = [Direction.NORTHEAST, Direction.SOUTHEAST, Direction.SOUTHWEST, Direction.NORTHWEST ]
eight_point_directions = cardinal_directions + ordinal_directions

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
        return GridUtil.position_in_bounds(location, self.width, self.height)
    
    def render_positions(self, point_list, placeholder):
        parts = []
        for i in range(0, self.height):
            for j in range(0, self.width):
                point = Point(j,i)
                if point in point_list:
                    parts.append(self.get_value(point))
                else:
                    parts.append(placeholder)
            parts.append("\n")
        return "".join(parts)
    
    def get_matching_positions(self, value):
        # iterates entire grid so should be avoided inside loops where possible
        return [Point(col,row) for row in range(0,self.height) for col in range(0, self.width) if self.get_value(Point(col, row)) == value ]

    def __repr__(self):
        parts = []
        for row in self.grid:
            for val in row:
                parts.append(val)
            parts.append("\n")
        return "".join(parts)
    
class GridUtil:
    @staticmethod
    def position_in_bounds(location:Point, width, height):
        return ( location.col >= 0 and location.row >= 0 and location.col < width and location.row < height )
    
    @staticmethod
    def get_positions_matching_from_lines(lines, matcher_func:Callable[[str], bool]):
        width = len(lines[0])
        height = len(lines)
        points = []

        for row in range(0,height):
            for col in range(0, width):
                if matcher_func(lines[row][col]):
                    points.append(Point(col,row))

        return points