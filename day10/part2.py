from collections import deque
from util.grids import Grid, Point, cardinal_directions

def solve(lines:list[str]):
    map_grid = Grid(lines)
    trailheads = map_grid.get_matching_positions("0")

    overall_total = 0
    for trailhead in trailheads:
        current_point = Point(trailhead.col, trailhead.row)
        points_to_test = deque([Point(current_point.col, current_point.row)])
        trail_rating = 0

        while len(points_to_test) > 0:
            point_to_test = points_to_test.pop()

            if map_grid.get_value(point_to_test) == "9":
                # go round again and dont try traverse from here
                trail_rating += 1
                continue

            points_from_here = [
                    Point(point_to_test.col + dir.value.col, point_to_test.row + dir.value.row) 
                    for dir in cardinal_directions 
                    if map_grid.position_in_bounds(Point(point_to_test.col + dir.value.col, point_to_test.row + dir.value.row))
                ]

            for point in points_from_here:
                point_val = map_grid.get_value(point)
                #its numeric, and its 1 more than the current value. Add it to the points to test
                # numeric test is to guard against the example input which contains "." characters
                if point_val.isdigit() and int(point_val) == int(map_grid.get_value(point_to_test)) + 1:
                    points_to_test.append(point)

                    
        # print(f"trailhead {trailhead} had a trail rating of {trail_rating}")
        overall_total += trail_rating
        
    print(overall_total)