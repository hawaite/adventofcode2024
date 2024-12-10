from util.grids import Grid, Point, cardinal_directions

def solve(lines:list[str]):
    map_grid = Grid(lines)
    trailheads = [Point(col,row) for row in range(0,map_grid.height) for col in range(0, map_grid.width) if map_grid.get_value(Point(col, row)) == "0" ]

    overall_total = 0
    for trailhead in trailheads:
        current_point = Point(trailhead.col, trailhead.row)
        points_to_test = [Point(current_point.col, current_point.row)]
        trail_rating = 0

        while True:
            if len(points_to_test) == 0:
                break # ran out of things to test
            # evaluate next point in the TODO list
            point_to_test = points_to_test[0]
            points_to_test = points_to_test[1:]

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