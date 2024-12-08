from enum import Enum
from util.grids import Grid, Point, Direction

def get_4_points_in_direction(dir:Direction, start:Point):
    return [Point(start.col + (dir.value.col * i), start.row + (dir.value.row * i)) for i in range(0,4)]

def all_points_in_bounds(points_list, crossword_grid):
    return all([crossword_grid.position_in_bounds(x) for x in points_list])

def points_spell_xmas(points_list, crossword):
    return "".join([crossword.get_value(point) for point in points_list]) == "XMAS"

def search_all_directions(row,col,crossword_grid):
    # early escape
    if crossword_grid.get_value(Point(col,row)) != "X":
        return 0
    
    total_valid = 0
    start_point = Point(col, row)
    for dir in Direction:
        points = get_4_points_in_direction(dir, start_point)

        if all_points_in_bounds(points, crossword_grid):
            if points_spell_xmas(points, crossword_grid):
                total_valid += 1
    return total_valid
    

def solve(lines:list[str]):
    crossword = Grid(lines)
    total = 0
    for row in range(0,len(lines)):
        for col in range(0, len(lines[0])):
            valid_count = search_all_directions(row,col,crossword)
            total += valid_count

    print(total)