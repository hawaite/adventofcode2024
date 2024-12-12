from util.grids import Direction, Grid, Point, cardinal_directions

# a single point can be 4 external corners at once
def external_corners_on_point(point:Point, grid:Grid) -> int:
    total = 0
    current_point_value = grid.get_value(point)

    up_point = Point(point.col + Direction.NORTH.value.col, point.row + Direction.NORTH.value.row)
    down_point = Point(point.col + Direction.SOUTH.value.col, point.row + Direction.SOUTH.value.row)
    left_point = Point(point.col + Direction.WEST.value.col, point.row + Direction.WEST.value.row)
    right_point = Point(point.col + Direction.EAST.value.col, point.row + Direction.EAST.value.row)

    up_inbounds = grid.position_in_bounds(up_point)
    down_inbounds = grid.position_in_bounds(down_point)
    left_inbounds = grid.position_in_bounds(left_point)
    right_inbounds = grid.position_in_bounds(right_point)

    up_oob_or_different_value = False
    if not up_inbounds:
        up_oob_or_different_value = True
    else: #inbounds
        if grid.get_value(up_point) != current_point_value:
            up_oob_or_different_value = True

    down_oob_or_different_value = False
    if not down_inbounds:
        down_oob_or_different_value = True
    else: #inbounds
        if grid.get_value(down_point) != current_point_value:
            down_oob_or_different_value = True

    left_oob_or_different_value = False
    if not left_inbounds:
        left_oob_or_different_value = True
    else: #inbounds
        if grid.get_value(left_point) != current_point_value:
            left_oob_or_different_value = True

    right_oob_or_different_value = False
    if not right_inbounds:
        right_oob_or_different_value = True
    else: #inbounds
        if grid.get_value(right_point) != current_point_value:
            right_oob_or_different_value = True

    # UP & LEFT
    if up_oob_or_different_value and left_oob_or_different_value:
        total += 1

    # UP & RIGHT
    if up_oob_or_different_value and right_oob_or_different_value:
        total += 1

    # DOWN & LEFT
    if down_oob_or_different_value and left_oob_or_different_value:
        total += 1

    # DOWN & RIGHT
    if down_oob_or_different_value and right_oob_or_different_value:
        total += 1

    return total

def internal_corners_on_point(point:Point, grid:Grid) -> bool:
    # up & left must be value, while upleft is not
    current_point_value = grid.get_value(point)
    total = 0

    up_point = Point(point.col + Direction.NORTH.value.col, point.row + Direction.NORTH.value.row)
    down_point = Point(point.col + Direction.SOUTH.value.col, point.row + Direction.SOUTH.value.row)
    left_point = Point(point.col + Direction.WEST.value.col, point.row + Direction.WEST.value.row)
    right_point = Point(point.col + Direction.EAST.value.col, point.row + Direction.EAST.value.row)

    up_left_point = Point(point.col + Direction.NORTHWEST.value.col, point.row + Direction.NORTHWEST.value.row)
    down_left_point = Point(point.col + Direction.SOUTHWEST.value.col, point.row + Direction.SOUTHWEST.value.row)
    up_right_point = Point(point.col + Direction.NORTHEAST.value.col, point.row + Direction.NORTHEAST.value.row)
    down_right_point = Point(point.col + Direction.SOUTHEAST.value.col, point.row + Direction.SOUTHEAST.value.row)

    # up-left. All points must be in-bounds to be an internal corner
    if grid.position_in_bounds(up_point) and grid.position_in_bounds(up_left_point) and grid.position_in_bounds(left_point):
        if grid.get_value(up_point) == current_point_value and grid.get_value(left_point) == current_point_value and grid.get_value(up_left_point) != current_point_value:
            #is up-left internal corner
            total += 1
        
    # up-right. All points must be in-bounds to be an internal corner
    if grid.position_in_bounds(up_point) and grid.position_in_bounds(up_right_point) and grid.position_in_bounds(right_point):
        if grid.get_value(up_point) == current_point_value and grid.get_value(right_point) == current_point_value and grid.get_value(up_right_point) != current_point_value:
            #is up-right internal corner
            total += 1
        
    # down-left. All points must be in-bounds to be an internal corner
    if grid.position_in_bounds(down_point) and grid.position_in_bounds(down_left_point) and grid.position_in_bounds(left_point):
        if grid.get_value(down_point) == current_point_value and grid.get_value(left_point) == current_point_value and grid.get_value(down_left_point) != current_point_value:
            #is down-left internal corner
            total += 1
        
    # down-right. All points must be in-bounds to be an internal corner
    if grid.position_in_bounds(down_point) and grid.position_in_bounds(down_right_point) and grid.position_in_bounds(right_point):
        if grid.get_value(down_point) == current_point_value and grid.get_value(right_point) == current_point_value and grid.get_value(down_right_point) != current_point_value:
            #is down-right internal corner
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