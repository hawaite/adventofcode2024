from util.grids import Grid, Point, cardinal_directions

def solve(lines:list[str]):
    grid = Grid(lines)
    # a set to hold all the points we've already used since points can only be in one group
    all_consumed_points = set()
    total = 0

    for row in range(0,grid.height):
        for col in range(0,grid.width):
            # for each point, attempt a flood-fill from there to get all the points belonging to that group
            points_in_group = set()
            start_point = Point(col,row)
            perimeter = 0
            # this point belonged to another group already. skip it.
            if start_point in all_consumed_points:
                continue

            to_check = set([start_point])
            val_to_find = grid.get_value(start_point)

            while len(to_check) > 0:
                current_point = to_check.pop()
                points_in_group.add(current_point)

                directions_from_here = [ Point(current_point.col + dir.value.col, current_point.row + dir.value.row) for dir in cardinal_directions ]

                # get all surrounding points which are inbound, havent been traversed before, and match the required value
                inbound_unvisited_points = [
                    p for p in directions_from_here 
                    if grid.position_in_bounds(p) and p not in points_in_group and grid.get_value(p) == val_to_find 
                ]

                # add all these points to the set of positions to check
                to_check = to_check.union(inbound_unvisited_points)

                #check the perimeter of this individual point
                for direction_point in directions_from_here:
                    if (not grid.position_in_bounds(direction_point)) or grid.get_value(direction_point) != val_to_find:
                        # point in that direction belongs to another group or is an edge
                        perimeter += 1

            # add the entire group of points to the set of all points consumed so far
            all_consumed_points = all_consumed_points.union(points_in_group)
            area = len(points_in_group)
            total += (perimeter * area)

    print(total)