from util.grids import Grid, Point, cardinal_directions, ordinal_directions

def corners_on_point(point:Point, grid:Grid) -> int:
    total = 0
    current_point_value = grid.get_value(point)
    directions_to_test = ordinal_directions

    for direction_to_test in directions_to_test:
        test_points = [Point(point.col + direction_to_test.rotate(angle).value.col, point.row + direction_to_test.rotate(angle).value.row) for angle in [-45, 0, 45]]

        # test for external corner in direction
        oob_or_not_matching_points = [tp for tp in [test_points[0], test_points[2]] if not grid.position_in_bounds(tp) or (grid.position_in_bounds(tp) and grid.get_value(tp) != current_point_value)]
        if len(oob_or_not_matching_points) == 2:
            total += 1
            continue # cannot be both an internal and external corner in this one direction

        # test for internal corner in direction
        if not all([grid.position_in_bounds(p) for p in test_points]):
            continue # this direction is not all inbounds, but others may be
        # if point 0 and 2 match but point 1 does not, thats an internal corner
        if grid.get_value(test_points[0]) == current_point_value and grid.get_value(test_points[2]) == current_point_value and grid.get_value(test_points[1]) != current_point_value:
            total += 1

    return total

def solve(lines:list[str]):
    grid = Grid(lines)
    all_consumed_points = set()
    total = 0
    for row in range(0,grid.height):
        for col in range(0,grid.width):
            # for each point, attempt a flood-fill from there to get all the points in this group
            points_in_group = set()
            start_point = Point(col,row)
            
            if start_point in all_consumed_points:
                continue

            to_check = set([start_point])
            val_to_find = grid.get_value(start_point)

            while len(to_check) > 0:
                current_point:Point = to_check.pop()
                points_in_group.add(current_point)

                points = [ Point(current_point.col + dir.value.col, current_point.row + dir.value.row) for dir in cardinal_directions ]
                # only get points which are inbound, havent been traversed before, and match the required value

                inbound_unvisited_points = [p for p in points if grid.position_in_bounds(p) and p not in points_in_group and grid.get_value(p) == val_to_find ]
                to_check = to_check.union(inbound_unvisited_points)
            
            all_consumed_points = all_consumed_points.union(points_in_group)

            area = len(points_in_group)

            # number of sides is equal to number of corners
            corners = sum([corners_on_point(p, grid) for p in points_in_group])
            
            # print(f"val to find: {val_to_find}, area: {area}, corners: {corners}")
            total += (corners * area)

    print(total)