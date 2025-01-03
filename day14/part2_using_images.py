# do not run unless you want to generate 10,403 PNGs in this directory
from dataclasses import dataclass
from PIL import Image
import os

@dataclass
class Robot:
    x: int
    y: int
    speed_x: int
    speed_y: int

def solve(lines:list[str]):
    robots = []
    grid_width = 101
    grid_height = 103
    os.mkdir("./day14/temp")

    for line in lines:
        position_part, speed_part = line.split(" ")
        x_pos, y_pos = position_part[2:].split(",")
        x_speed, y_speed = speed_part[2:].split(",")
        robots.append(Robot(int(x_pos), int(y_pos), int(x_speed), int(y_speed)))

    # today, we're going to generate 101 * 103 PNG files 
    # and then look through them in file explorer until we spot something looking like a christmas tree
    # after 101 * 103 ticks the robots will all be in their starting position
    for tick in range(0,grid_width * grid_height):
        img = Image.new("1", (grid_width, grid_height)) # 1 bpp black rectangle
        # move robots
        for robot in robots:
            new_x_pos = (robot.x + robot.speed_x) % grid_width
            new_y_pos = (robot.y + robot.speed_y) % grid_height
            robot.x = new_x_pos
            robot.y = new_y_pos
            img.putpixel((robot.x, robot.y), 1) # add white pixel where robot is
        
        # render image
        img.save(f"./day14/temp/output_{tick+1}.png")