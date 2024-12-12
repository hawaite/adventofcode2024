from util.grids import Direction, Grid, Point, cardinal_directions

# external corners like the 4 on the outside of a square. a 90 degree angle wrt the shape
# a single point can be 4 external corners at once
# a point counts as an external corner if we take 2 consecutive cardinal directions
# and both of them dont match the current point value. Out of bounds counts as not matching
def external_corners_on_point(point:Point, grid:Grid) -> int:
    total = 0
    current_point_value = grid.get_value(point)
    directions_to_test = [Direction.NORTHEAST, Direction.SOUTHEAST, Direction.SOUTHWEST, Direction.NORTHWEST]
    for direction_to_test in directions_to_test:
        # get a list of the two points we're testing
        test_points = [Point(point.col + direction_to_test.rotate(angle).value.col, point.row + direction_to_test.rotate(angle).value.row) for angle in [-45, 45]]
        # get only points which are either out of bounds, or do NOT match the current point value
        oob_or_not_matching_points = [tp for tp in test_points if not grid.position_in_bounds(tp) or (grid.position_in_bounds(tp) and grid.get_value(tp) != current_point_value)]
        # if we still have two points then this is an external corner
        if len(oob_or_not_matching_points) == 2:
            total += 1
    return total

# internal corners are like that one 270 degree angle on the inside of an "L" shape
# a single point can be multiple external corners, as seen in the "E" example input
# we test for this by taking three consecutive directional points and if the outer two match the the current point value
# and the middle one does not, we have an internal corner. It is not possible for an internal corner to be out of bounds.
def internal_corners_on_point(point:Point, grid:Grid) -> int:
    # up & left must be value, while upleft is not
    current_point_value = grid.get_value(point)
    total = 0
    directions_to_test = [Direction.NORTHEAST, Direction.SOUTHEAST, Direction.SOUTHWEST, Direction.NORTHWEST]
    for direction_to_test in directions_to_test:
        test_points = [Point(point.col + direction_to_test.rotate(angle).value.col, point.row + direction_to_test.rotate(angle).value.row) for angle in [-45, 0, 45]]
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
            # for each point, attempt a flood-fill from there to get all the points
            # replace those points in the grid with '.'
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

            # work out perimeter
            external_corners = 0
            internal_corners = 0
            area = len(points_in_group)
            # number of sides is equal to number of corners
            for point in points_in_group:
                # two types of corner with different rules for checking, but all count towards sides
                external_corners += external_corners_on_point(point, grid)
                internal_corners += internal_corners_on_point(point, grid)
            
            print(f"val to find: {val_to_find}, area: {area}, external corners: {external_corners}, internal corners: {internal_corners}")
            total += ((internal_corners + external_corners) * area)

    print(total)