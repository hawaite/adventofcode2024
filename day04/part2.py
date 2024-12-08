from typing import Tuple
from util.grids import Grid, Point

def get_x_centered_at_point(center):
    span_one = [Point(center.col-1, center.row-1), Point(center.col, center.row), Point(center.col+1, center.row+1)] #top left to bottom right
    span_two = [Point(center.col+1, center.row-1), Point(center.col, center.row), Point(center.col-1, center.row+1)] #top right to bottom left
    return (span_one, span_two)

def all_points_in_bounds(cross:Tuple[list[Point],list[Point]], crossword_grid:Grid):
    return all([crossword_grid.position_in_bounds(x) for x in (cross[0] +cross[1])])

def points_spell_mas_either_direction(points_list, crossword):
    return "".join([crossword.get_value(point) for point in points_list]) in ["MAS","SAM"]

def is_x_mas_in_any_orientation(point,crossword):
    if crossword.get_value(point) != "A": # early escape
        return False
    
    cross_points = get_x_centered_at_point(point)
    if not all_points_in_bounds(cross_points, crossword):
        return False
    
    return points_spell_mas_either_direction(cross_points[0], crossword) and points_spell_mas_either_direction(cross_points[1], crossword)
    

def solve(lines:list[str]):
    crossword = Grid(lines)
    total = 0
    for row in range(0,len(lines)):
        for col in range(0, len(lines[0])):
            if is_x_mas_in_any_orientation(Point(col,row),crossword):
                total += 1
    print(total)