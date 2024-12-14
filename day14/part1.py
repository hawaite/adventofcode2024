import math

def solve(lines:list[str]):
    # grid_width = 11
    # grid_height = 7
    grid_width = 101
    grid_height = 103
    x_centerline = math.floor(grid_width / 2)
    y_centerline = math.floor(grid_height / 2)
    quadrant_count = {1: 0, 2: 0, 3: 0, 4: 0}

    for line in lines:
        position_part, speed_part = line.split(" ")
        x_pos, y_pos = position_part[2:].split(",")
        x_speed, y_speed = speed_part[2:].split(",")
        new_x_pos = (int(x_pos) + (100 * int(x_speed))) % grid_width
        new_y_pos = (int(y_pos) + (100 * int(y_speed))) % grid_height

        if new_x_pos >= 0 and new_x_pos < x_centerline:
            # left quadrants
            if new_y_pos >= 0 and new_y_pos < y_centerline:
                #top left. quadrant 1
                quadrant_count[1] = quadrant_count[1] + 1
                continue
            elif new_y_pos > y_centerline:
                # bottom left. quadrant 3
                quadrant_count[3] = quadrant_count[3] + 1
                continue
        elif new_x_pos > x_centerline:
            # right quadrants
            if new_y_pos >= 0 and new_y_pos < y_centerline:
                # top right. quadrant 2
                quadrant_count[2] = quadrant_count[2] + 1
                continue
            elif new_y_pos > y_centerline:
                # bottom right. quadrant 4
                quadrant_count[4] = quadrant_count[4] + 1
                continue
    
    print(f"safety factor: {quadrant_count[1] * quadrant_count[2] * quadrant_count[3] * quadrant_count[4]}")