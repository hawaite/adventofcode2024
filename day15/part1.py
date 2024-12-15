from typing import List, Tuple
from util.grids import Grid, Direction, Point

# updates grid in place, returns new robot position
def perform_single_move_if_possible(boxes: list[Point], walls: list[Point], robot_point:Point, move:Direction) -> Tuple[List[Point], Point]:
    target_robot_position_point = Point(robot_point.col + move.value.col, robot_point.row + move.value.row)
    # proposed space is a wall. Return boxes and robot location without change
    if target_robot_position_point in walls:
        return (boxes, robot_point)
    
    # proposed space is not a box and not a wall.
    if target_robot_position_point not in boxes:
        return (boxes, target_robot_position_point)
    
    # proposed position MUST be a box at this point
    pos_to_test = Point(target_robot_position_point.col + move.value.col, target_robot_position_point.row + move.value.row)
    # iterate along this axis until we hit a wall or a space
    while True:
        if pos_to_test in walls:
            # boxes are against a wall. return unchanged
            return (boxes, robot_point)
        elif pos_to_test in boxes:
            pos_to_test = Point(pos_to_test.col + move.value.col, pos_to_test.row + move.value.row)
            continue # another box. Keep going.
        else:
            # must be a space.
            # this point is now a box
            new_boxes = boxes + [ pos_to_test ]
            # robot moves to new position
            new_robot_point = target_robot_position_point
            # remove the new robots position from the list of boxes
            new_boxes.remove(new_robot_point)
            return (new_boxes, new_robot_point)

def solve(lines:list[str]):
    defining_board = True
    board_def = []
    move_def = []
    for line in lines:
        if line == "":
            defining_board = False
            continue
        if defining_board:
            board_def.append(line)
        else:
            move_def.append(line)

    grid = Grid(board_def)
    robot_point = grid.get_matching_positions("@")[0]
    wall_points = grid.get_matching_positions("#")
    box_points = grid.get_matching_positions("O")

    for move in "".join(move_def):
        if move == "^":
            (box_points, robot_point) = perform_single_move_if_possible(box_points, wall_points, robot_point, Direction.NORTH)
        elif move == ">":
            (box_points, robot_point) = perform_single_move_if_possible(box_points, wall_points, robot_point, Direction.EAST)
        elif move == "v":
            (box_points, robot_point) = perform_single_move_if_possible(box_points, wall_points, robot_point, Direction.SOUTH)
        elif move == "<":
            (box_points, robot_point) = perform_single_move_if_possible(box_points, wall_points, robot_point, Direction.WEST)

    total = 0
    for box in box_points:
        box_location = (box.row * 100) + box.col
        total += box_location
    print(total)