from dataclasses import dataclass
from typing import List, Tuple
from util.grids import Grid, Direction, Point

@dataclass(frozen=True)
class Box:
    left: Point
    right: Point

def generate_map(lines):
    updated_map_lines = []
    for line in lines:
        new_map_line = []
        for char in line:
            if char == "#":
                new_map_line.extend(["#", "#"])
            elif char == "O":
                new_map_line.extend(["[", "]"])
            elif char == ".":
                new_map_line.extend([".", "."])
            elif char == "@":
                new_map_line.extend(["@", "."])
        updated_map_lines.append("".join(new_map_line))
    return updated_map_lines

def can_push_box_in_direction(box:Box, boxes:list[Box], walls:list[Point], move:Direction) -> bool:
    # starting at box, iterate over adjacent boxes until either we hit a wall, or run out of adjacent boxes
    # north/south is different to east/west due to non-square boxes.
    # TODO
    all_boxes_left_points = [b.left for b in boxes]
    all_boxes_right_points = [b.right for b in boxes]
    if move == Direction.WEST:
        #simple line as boxes are 1 unit hight
        current_box = box
        # check left from current box left point by 1
        # can see if its a wall or if its a "right-side point of a box"
        point_to_test = Point(box.left.col - 1, box.left.row)
        if point_to_test in all_boxes_right_points:
            # we found an adjacent box.
            # do something about that
            adjacent_box = [b for b in boxes if b.right == point_to_test][0]
            # print(f"Found adjacent box {adjacent_box}")
            return can_push_box_in_direction(adjacent_box, boxes, walls, move)
        elif point_to_test in walls:
            # print("Hit wall")
            return False # immediately false because you cant push in to a wall
        else:
            # must be a space
            # print("hit space")
            return True
    elif move == Direction.EAST:
        # check right from current box right point by 1
        # can see if its a wall or if its a "left-side point of a box"
        point_to_test = Point(box.right.col + 1, box.right.row)
        if point_to_test in all_boxes_left_points:
            # we found an adjacent box.
            # do something about that
            adjacent_box = [b for b in boxes if b.left == point_to_test][0]
            # print(f"Found adjacent box {adjacent_box}")
            return can_push_box_in_direction(adjacent_box, boxes, walls, move)
        elif point_to_test in walls:
            # print("Hit wall")
            return False # immediately false because you cant push in to a wall
        else:
            # must be a space
            # print("hit space")
            return True
    elif move == Direction.NORTH:
        point_to_test_left = Point(box.left.col, box.left.row - 1)
        point_to_test_right = Point(box.right.col, box.right.row - 1)

        if point_to_test_left in walls or point_to_test_right in walls:
            return False

        # get all points that in any of the 3 possible adjacencies above.
        adjacent_boxes = [b for b in boxes if b.right == point_to_test_left or b.left == point_to_test_right or (b.left == point_to_test_left and b.right == point_to_test_right)]
        # there were adjacent boxes in this direction
        if len(adjacent_boxes) > 0:
            # return true if all the adjacent boxes we just found are pushable
            return all([can_push_box_in_direction(adjacent_box, boxes, walls, move) for adjacent_box in adjacent_boxes])
        else:
            # there were no walls or boxes in this direction, meaning 2 valid spaces.
            return True
    else:
        point_to_test_left = Point(box.left.col, box.left.row + 1)
        point_to_test_right = Point(box.right.col, box.right.row + 1)

        if point_to_test_left in walls or point_to_test_right in walls:
            return False

        # get all points that in any of the 3 possible adjacencies above.
        adjacent_boxes = [b for b in boxes if b.right == point_to_test_left or b.left == point_to_test_right or (b.left == point_to_test_left and b.right == point_to_test_right)]
        # there were adjacent boxes in this direction
        if len(adjacent_boxes) > 0:
            # return true if all the adjacent boxes we just found are pushable
            return all([can_push_box_in_direction(adjacent_box, boxes, walls, move) for adjacent_box in adjacent_boxes])
        else:
            # there were no walls or boxes in this direction, meaning 2 valid spaces.
            return True

def get_all_adjacent_boxes(box:Box, boxes:list[Box], move: Direction):
    all_boxes_left_points = [b.left for b in boxes]
    all_boxes_right_points = [b.right for b in boxes]
    if move == Direction.WEST:
        #simple line as boxes are 1 unit hight
        # check left from current box left point by 1
        # can see if its a wall or if its a "right-side point of a box"
        point_to_test = Point(box.left.col - 1, box.left.row)
        if point_to_test in all_boxes_right_points:
            # we found an adjacent box.
            # do something about that
            adjacent_box = [b for b in boxes if b.right == point_to_test][0]
            # print(f"Found adjacent box {adjacent_box}")
            return [adjacent_box] + get_all_adjacent_boxes(adjacent_box, boxes, move)
        else:
            return []
    elif move == Direction.EAST:
        # check right from current box right point by 1
        # can see if its a wall or if its a "left-side point of a box"
        point_to_test = Point(box.right.col + 1, box.right.row)
        if point_to_test in all_boxes_left_points:
            # we found an adjacent box.
            # do something about that
            adjacent_box = [b for b in boxes if b.left == point_to_test][0]
            # print(f"Found adjacent box {adjacent_box}")
            return [adjacent_box] + get_all_adjacent_boxes(adjacent_box, boxes, move)
        else:
            return []
    elif move == Direction.NORTH:
        point_to_test_left = Point(box.left.col, box.left.row - 1)
        point_to_test_right = Point(box.right.col, box.right.row - 1)

        # get all points that in any of the 3 possible adjacencies above.
        adjacent_boxes = [b for b in boxes if b.right == point_to_test_left or b.left == point_to_test_right or (b.left == point_to_test_left and b.right == point_to_test_right)]
        # there were adjacent boxes in this direction
        if len(adjacent_boxes) == 1:
            return [adjacent_boxes[0]] + get_all_adjacent_boxes(adjacent_boxes[0], boxes, move)
        elif len(adjacent_boxes) == 2:
            return [adjacent_boxes[0], adjacent_boxes[1]] + get_all_adjacent_boxes(adjacent_boxes[0], boxes, move) + get_all_adjacent_boxes(adjacent_boxes[1], boxes, move)
        else:
            # there were no walls or boxes in this direction, meaning 2 valid spaces.
            return []
    elif move == Direction.SOUTH:
        point_to_test_left = Point(box.left.col, box.left.row + 1)
        point_to_test_right = Point(box.right.col, box.right.row + 1)

        # get all points that in any of the 3 possible adjacencies above.
        adjacent_boxes = [b for b in boxes if b.right == point_to_test_left or b.left == point_to_test_right or (b.left == point_to_test_left and b.right == point_to_test_right)]
        # there were adjacent boxes in this direction
        if len(adjacent_boxes) == 1:
            return [adjacent_boxes[0]] + get_all_adjacent_boxes(adjacent_boxes[0], boxes, move)
        elif len(adjacent_boxes) == 2:
            return [adjacent_boxes[0], adjacent_boxes[1]] + get_all_adjacent_boxes(adjacent_boxes[0], boxes, move) + get_all_adjacent_boxes(adjacent_boxes[1], boxes, move)
        else:
            # there were no walls or boxes in this direction, meaning 2 valid spaces.
            return []

def push_box_in_direction(box:Box, boxes:list[Box], move:Direction) -> list[Box]:
    # for all boxes adjacent to this one in a direction, increase the coord in that direction
    # TODO
    updated_boxes = boxes.copy()
    boxes_to_move = list(set([box] + get_all_adjacent_boxes(box, updated_boxes, move)))
    # print(f"pushing boxes: {boxes_to_move} in direction {move.name}")
    for box_to_move in boxes_to_move:
        # delete old box
        updated_boxes.remove(box_to_move)
        # add new box wirh updated position
        updated_boxes.append(Box(Point(box_to_move.left.col + move.value.col, box_to_move.left.row + move.value.row), Point(box_to_move.right.col + move.value.col, box_to_move.right.row + move.value.row)))
    return updated_boxes

def perform_single_move_if_possible(boxes: list[Box], walls: list[Point], robot_point:Point, move:Direction) -> Tuple[List[Box], Point]:
    target_robot_position_point = Point(robot_point.col + move.value.col, robot_point.row + move.value.row)

    # proposed space is a wall. Return boxes and robot location without change
    if target_robot_position_point in walls:
        return (boxes, robot_point)
    
    # proposed space is not a box and not a wall.
    # is an empty space. move robot there.
    all_box_points = [x.left for x in boxes] + [x.right for x in boxes]
    if target_robot_position_point not in all_box_points:
        return (boxes, target_robot_position_point)
    
    # proposed position MUST be a box at this point
    # find which box
    adjacent_box = [ box for box in boxes if box.left == target_robot_position_point or box.right == target_robot_position_point ][0]

    if can_push_box_in_direction(adjacent_box, boxes, walls, move):
        updated_boxes = push_box_in_direction(adjacent_box, boxes, move)
        return (updated_boxes, target_robot_position_point) # return new boxes list and new robot position
    
    # we cannot push box in this direction
    return (boxes, robot_point) # return original 

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

    updated_board_def = generate_map(board_def)
    grid = Grid(updated_board_def)

    robot_point = grid.get_matching_positions("@")[0]
    wall_points = grid.get_matching_positions("#")
    box_left_points = grid.get_matching_positions("[")

    boxes = [Box(point, Point(point.col+1, point.row)) for point in box_left_points]

    for move in "".join(move_def):
        [x.left for x in boxes] + [x.right for x in boxes]
        if move == "^": # up
            (boxes, robot_point) = perform_single_move_if_possible(boxes, wall_points, robot_point, Direction.NORTH)
        elif move == ">": # right
            (boxes, robot_point) = perform_single_move_if_possible(boxes, wall_points, robot_point, Direction.EAST)
        elif move == "v": # down
            (boxes, robot_point) = perform_single_move_if_possible(boxes, wall_points, robot_point, Direction.SOUTH)
        elif move == "<": # left
            (boxes, robot_point) = perform_single_move_if_possible(boxes, wall_points, robot_point, Direction.WEST)

    total = 0
    for box in boxes:
        box_location = (box.left.row * 100) + box.left.col
        total += box_location

    print(total)