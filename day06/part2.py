from enum import Enum

# reminder: positions are (col, row)
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

def solve(lines:list[str]):
    obstacle_positions = []
    starting_guard_position = (0,0)
    
    width = len(lines[0])
    height = len(lines)

    # get starting position and obstacle positions
    for row in range(0, height):
        for col in range(0, width):
            if lines[row][col] == "#":
                obstacle_positions.append((col,row))
            elif lines[row][col] == "^":
                starting_guard_position = (col, row)

    new_obstacles_causing_cycles = []
    for new_obstacle_row in range(0, height):
        for new_obstacle_col in range(0, width):
            print((new_obstacle_col, new_obstacle_row))

            # test if this is an existing obstacle or the starting position here
            if (new_obstacle_col, new_obstacle_row) in obstacle_positions or (new_obstacle_col, new_obstacle_row) == starting_guard_position:
                continue
            
            # reset everything between new obstacle tests
            new_obstacle_positions = obstacle_positions.copy() # take a copy of the original obstacle list and add a new one
            new_obstacle_positions.append((new_obstacle_col, new_obstacle_row))
            guard_position = (starting_guard_position[0],starting_guard_position[1])
            guard_direction = Direction.UP

            saved_guard_positions = []
            saved_guard_positions_with_direction = {}
            saved_guard_positions_with_direction[Direction.UP.name] = [] 
            saved_guard_positions_with_direction[Direction.DOWN.name] = [] 
            saved_guard_positions_with_direction[Direction.LEFT.name] = [] 
            saved_guard_positions_with_direction[Direction.RIGHT.name] = [] 

            # run the checker
            while True:
                # test if obstacle in wanted direction
                position_to_test = (guard_position[0] + guard_direction.value[0], guard_position[1] + guard_direction.value[1])
                if(pos_out_of_bounds(position_to_test,width,height)):
                    break # next point will be out of bounds
                else: # next point will be inbounds
                    if (position_to_test[0],position_to_test[1]) in new_obstacle_positions: # check if pointion to test is an obstacle
                        # print("changing direction from " + guard_direction.name + " to " + rotate_direction(guard_direction).name)
                        guard_direction = rotate_direction(guard_direction)
                    else: # could be . or ^
                        if position_to_test in saved_guard_positions_with_direction[guard_direction.name]:
                            #this point has been seen before, in this direction, meaning a cycle
                            new_obstacles_causing_cycles.append((new_obstacle_col, new_obstacle_row))
                            break
                        else:
                            guard_position = position_to_test
                            saved_guard_positions.append(guard_position)
                            saved_guard_positions_with_direction[guard_direction.name].append(guard_position)

    print(len(new_obstacles_causing_cycles))