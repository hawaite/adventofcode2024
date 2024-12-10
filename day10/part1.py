from util.grids import Grid, Point, cardinal_directions

def solve(lines:list[str]):
    map_grid = Grid(lines)
    trailheads = [Point(col,row) for row in range(0,map_grid.height) for col in range(0, map_grid.width) if map_grid.get_value(Point(col, row)) == "0" ]

    overall_total = 0
    for trailhead in trailheads:
        current_point = Point(trailhead.col, trailhead.row)
        found_finishes = set()
        points_to_test = [Point(current_point.col, current_point.row)]
        seen_points = set()
        
        while True:
            if len(points_to_test) == 0:
                break # ran out of things to test

            # pull first point and add it to the "seen" list
            point_to_test = points_to_test[0]
            points_to_test = points_to_test[1:]
            seen_points.add(Point(point_to_test.col, point_to_test.row))

            if map_grid.get_value(point_to_test) == "9":
                found_finishes.add(point_to_test)
                continue

            points_from_here = [
                Point(point_to_test.col + dir.value.col, point_to_test.row + dir.value.row) 
                for dir in cardinal_directions 
                if map_grid.position_in_bounds(Point(point_to_test.col + dir.value.col, point_to_test.row + dir.value.row))
                ]
            
            for point in points_from_here:
                # is inbounds and we havent seen this point before
                if point not in seen_points:
                    point_val = map_grid.get_value(point)
                    #its numeric, and its 1 more than the current value. Add it to the points to test
                    if point_val.isdigit() and int(point_val) == int(map_grid.get_value(point_to_test)) + 1:
                        points_to_test.append(point)

        overall_total += len(found_finishes)

    print(overall_total)