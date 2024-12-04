from enum import Enum

class Direction(Enum):
    UP = (0,-1)
    UP_RIGHT = (1,-1)
    RIGHT = (1,0)
    DOWN_RIGHT = (1,1)
    DOWN = (0,1)
    DOWN_LEFT = (-1,1)
    LEFT = (-1,0)
    UP_LEFT = (-1,-1)

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return "(%d,%d)" % (self.x,self.y)

    def inside_bounds(self, width, height):
        return not (self.x < 0 or self.x >= width or self.y < 0 or self.y >= height)

def get_4_points_in_direction(dir:Direction, start:Point):
    return [Point(start.x + (dir.value[0] * i), start.y + (dir.value[1] * i)) for i in range(0,4)]

def all_points_in_bounds(points_list, width, height):
    return all([x.inside_bounds(width,height) for x in points_list])

def points_spell_xmas(points_list, crossword):
    return "".join([crossword[point.y][point.x] for point in points_list]) == "XMAS"

def search_all_directions(row,col,width,height, crossword):
    # early escape
    if crossword[row][col] != "X":
        return 0
    
    total_valid = 0
    start_point = Point(col, row)
    for dir in Direction:
        points = get_4_points_in_direction(dir, start_point)
        if all_points_in_bounds(points, width, height) and points_spell_xmas(points, crossword):
            total_valid += 1
    return total_valid
    

def solve(lines:list[str]):
    width = len(lines[0])
    height = len(lines)
    total = 0
    for row in range(0,len(lines)):
        for col in range(0, len(lines[0])):
            valid_count = search_all_directions(col,row,width,height, lines)
            total += valid_count

    print(total)