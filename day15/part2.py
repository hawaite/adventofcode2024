from dataclasses import dataclass
from typing import List, Tuple
from util.grids import Grid, Direction, Point

@dataclass(frozen=True)
class Box:
    left: Point
    right: Point

    def point_is_in_this_box(self, point:Point):
        return point in [self.left, self.right]

def generate_expanded_map(lines):
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

# starting at box, iterate over adjacent boxes until either we hit a wall and return false, 
# or run out of adjacent boxes and return true because we ran out of adjacent boxes while not hitting a single wall
def can_push_box_in_direction(box:Box, boxes:list[Box], walls:list[Point], move:Direction) -> bool:
    # east/west moves are simple lines because boxes are 1 height but 2 width
    if move in [ Direction.WEST, Direction.EAST ]:
        # need to check 1 off the left if checking WEST or 1 off the right if checking RIGHT
        box_side_to_check = box.left if move == Direction.WEST else box.right
        point_to_test = Point(box_side_to_check.col + move.value.col, box_side_to_check.row + move.value.row)
        boxes_this_point_is_in = [ box for box in boxes if box.point_is_in_this_box(point_to_test)]
        if len(boxes_this_point_is_in) == 1: # found adjacent box
            return can_push_box_in_direction(boxes_this_point_is_in[0], boxes, walls, move)
        elif point_to_test in walls:
            return False # immediately false because you cant push in to a wall
        else:
            return True # must be a space
    # north/south moves need to check both points in the required direction for walls, spaces, and other boxes
    elif move in [ Direction.NORTH, Direction.SOUTH ]:
        point_to_test_left = Point(box.left.col, box.left.row + move.value.row)
        point_to_test_right = Point(box.right.col, box.right.row + move.value.row)

        # immediate failure if points in this direction are walls
        if point_to_test_left in walls or point_to_test_right in walls:
            return False

        # get all points that in any of the 3 possible adjacencies above/below. left, middle or right.
        adjacent_boxes = [b for b in boxes if b.right == point_to_test_left or b.left == point_to_test_right or (b.left == point_to_test_left and b.right == point_to_test_right)]
        # there were adjacent boxes in this direction
        if len(adjacent_boxes) > 0:
            # return true if all the adjacent boxes we just found are also pushable
            return all([can_push_box_in_direction(adjacent_box, boxes, walls, move) for adjacent_box in adjacent_boxes])
        else:
            # points were not walls or adjacent boxes, meaning spaces.
            return True

def get_all_adjacent_boxes(box:Box, boxes:list[Box], move: Direction) -> list[Box]:
    # east/west moves are simple lines because boxes are 1 height but 2 width
    if move in [ Direction.WEST, Direction.EAST] :
        box_side_to_use = box.left if move == Direction.WEST else box.right
        point_to_test = Point(box_side_to_use.col + move.value.col, box_side_to_use.row + move.value.row)
        boxes_this_point_is_in = [ box for box in boxes if box.point_is_in_this_box(point_to_test)]
        if len(boxes_this_point_is_in) == 1:
            return boxes_this_point_is_in + get_all_adjacent_boxes(boxes_this_point_is_in[0], boxes, move)
        else:
            return []
    # north/south moves need to check both points in the required direction for walls, spaces, and other boxes
    elif move in [Direction.NORTH, Direction.SOUTH]:
        point_to_test_left = Point(box.left.col + move.value.col, box.left.row + move.value.row)
        point_to_test_right = Point(box.right.col + move.value.col, box.right.row + move.value.row)

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
    # TODO: fix this hack
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

    updated_board_def = generate_expanded_map(board_def)
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