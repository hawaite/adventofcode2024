from util.grids import Direction, DirectionalPoint, Grid, Point

def pos_out_of_bounds(pos, width, height):
    return pos[0] < 0 or pos[1] < 0 or pos[0] >= width or pos[1] >= height

def get_all_points_before_escape(grid:Grid, guard_start:DirectionalPoint):
    seen_positions = set()
    # run the checker
    guard = DirectionalPoint(guard_start.point, guard_start.direction)
    seen_positions.add(guard.point) # add first location

    while True:
        # test if obstacle in wanted direction
        position_to_test = Point(guard.point.col + guard.direction.value.col, guard.point.row + guard.direction.value.row)
        if not grid.position_in_bounds(position_to_test):
            break # next point will be out of bounds
        else: # next point will be inbounds
            if grid.get_value(position_to_test) == "#": # perform rotate
                guard.direction = guard.direction.rotate(90)
            else: # perform valid move
                guard.point = position_to_test
                seen_positions.add(guard.point)

    return seen_positions

def solve(lines:list[str]):
    grid = Grid(lines)

    for row_ix, row_val in enumerate(lines):
        if "^" in row_val:
            col_ix = row_val.index("^")
            guard = DirectionalPoint(Point(col_ix, row_ix), Direction.NORTH)
            grid.set_value(guard.point, ".")

    new_obstacles_causing_cycles = []
    # reduce search space by only testing points which a +/-1 space from points on the original escape path
    points_to_check = set()
    original_escape_points = get_all_points_before_escape(grid, guard)
    points_to_check.update(original_escape_points)
    # remove guard starting position
    points_to_check.remove(guard.point)

    number_to_check = len(points_to_check)
    current = 1
    for new_obstacle in points_to_check:
        print("Testing point %d of %d"%(current,number_to_check))
        hypothetical_guard = DirectionalPoint(guard.point, guard.direction)

        saved_guard_positions_with_direction = {
            Direction.NORTH.name : [],
            Direction.SOUTH.name : [],
            Direction.WEST.name : [],
            Direction.EAST.name : []
        }

        grid.set_value(new_obstacle, "#") # set new obstacle

        # run the checker
        while True:
            # test if obstacle in wanted direction
            position_to_test = Point(hypothetical_guard.point.col + hypothetical_guard.direction.value.col, hypothetical_guard.point.row + hypothetical_guard.direction.value.row)
            if not grid.position_in_bounds(position_to_test):
                break # next point will be out of bounds
            else: # next point will be inbounds
                if grid.get_value(position_to_test) == "#": # check if pointion to test is an obstacle
                    hypothetical_guard.direction = hypothetical_guard.direction.rotate(90)
                else: # not an obstacle
                    # cycle detection
                    if position_to_test in saved_guard_positions_with_direction[hypothetical_guard.direction.name]:
                        #this point has been seen before, in this direction, meaning a cycle
                        new_obstacles_causing_cycles.append(new_obstacle)
                        break
                    else:
                        hypothetical_guard.point = position_to_test
                        saved_guard_positions_with_direction[hypothetical_guard.direction.name].append(hypothetical_guard.point)
        
        grid.set_value(new_obstacle, ".") # reset object back to floor piece
        current+=1


    print(len(new_obstacles_causing_cycles))