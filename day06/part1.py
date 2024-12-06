from enum import Enum
# positions are (col, row)
class Direction(Enum):
    UP = (0,-1)
    DOWN = (0,1)
    LEFT = (-1,0)
    RIGHT = (1,0)

def rotate_direction(dir:Direction):
    if dir == Direction.UP:
        return Direction.RIGHT
    if dir == Direction.RIGHT:
        return Direction.DOWN
    if dir == Direction.DOWN:
        return Direction.LEFT
    if dir == Direction.LEFT:
        return Direction.UP

def pos_out_of_bounds(pos, width, height):
    return pos[0] < 0 or pos[1] < 0 or pos[0] >= width or pos[1] >= height

def get_all_points_before_escape(start_point, start_dir, obstacles, width, height):
    seen_positions = set()
    # run the checker
    guard_position = start_point
    guard_direction = start_dir

    while True:
        # test if obstacle in wanted direction
        position_to_test = (guard_position[0] + guard_direction.value[0], guard_position[1] + guard_direction.value[1])
        if(pos_out_of_bounds(position_to_test,width,height)):
            break # next point will be out of bounds
        else: # next point will be inbounds
            if (position_to_test[0],position_to_test[1]) in obstacles: # check if pointion to test is an obstacle
                guard_direction = rotate_direction(guard_direction)
            else: # could be . or ^
                guard_position = position_to_test
                seen_positions.add(guard_position)
    return seen_positions

def solve(lines:list[str]):
    unique_guard_positions = set()
    obstacle_positions = []
    guard_position = (0,0)
    guard_direction = Direction.UP
    width = len(lines[0])
    height = len(lines)

    for row in range(0, height):
        for col in range(0, width):
            if lines[row][col] == "#":
                obstacle_positions.append((col,row))
            elif lines[row][col] == "^":
                guard_position = (col, row)
                unique_guard_positions.add(guard_position)

    unique_guard_positions = get_all_points_before_escape(guard_position, guard_direction, obstacle_positions, width, height)

    print(len(unique_guard_positions))