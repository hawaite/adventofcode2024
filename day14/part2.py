from dataclasses import dataclass
import statistics

@dataclass
class Robot:
    x: int
    y: int
    speed_x: int
    speed_y: int

def solve(lines:list[str]):
    robots:list[Robot] = []
    grid_width = 101
    grid_height = 103

    for line in lines:
        position_part, speed_part = line.split(" ")
        x_pos, y_pos = position_part[2:].split(",")
        x_speed, y_speed = speed_part[2:].split(",")
        robots.append(Robot(int(x_pos), int(y_pos), int(x_speed), int(y_speed)))

    # after 101 * 103 ticks the robots will all be in their starting position
    # so no need to continue beyond there
    min_variance = -1
    min_variance_ix = 0
    for tick in range(0,grid_width * grid_height):
        # move robots
        for robot in robots:
            new_x_pos = (robot.x + robot.speed_x) % grid_width
            new_y_pos = (robot.y + robot.speed_y) % grid_height
            robot.x = new_x_pos
            robot.y = new_y_pos

        all_x_values = [robot.x for robot in robots]
        all_y_values = [robot.y for robot in robots]
        x_var = statistics.variance(all_x_values)
        y_var = statistics.variance(all_y_values)
        var = x_var * y_var

        if var < min_variance or min_variance == -1:
            # if we have a new smallest variance, or this is the first loop
            min_variance = var
            min_variance_ix = tick + 1

    # really this is just the iteration that produced the lowest variance in x and y values
    # but since the tree is just a cluster of close together points, it works for this input.
    print(f"Tree is PROBABLY at tick: {min_variance_ix}")