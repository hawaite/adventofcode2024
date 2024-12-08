from util.grids import Direction, DirectionalPoint, Grid, Point

def get_all_points_before_escape(grid:Grid, guard_start:DirectionalPoint):
    seen_positions = set()
    # run the checker
    guard = guard_start
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

    unique_guard_positions = get_all_points_before_escape(grid, guard)

    print(len(unique_guard_positions))