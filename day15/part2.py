from dataclasses import dataclass
from typing import List, Tuple
from util.grids import Grid, Direction, Point

@dataclass(frozen=True)
class Box:
    left: Point
    right: Point

    def point_is_in_this_box(self, point:Point):
        return point in [self.left, self.right]
    
    def get_points_in_direction(self, direction:Direction) -> list[Point]:
        if direction in [ Direction.NORTH, Direction.SOUTH]:
            return [Point(self.left.col, self.left.row + direction.value.row), Point(self.right.col, self.right.row + direction.value.row)] 
        else:
            if direction == Direction.WEST:
                return [Point(self.left.col + direction.value.col, self.left.row + direction.value.row)]
            else:
                return [Point(self.right.col + direction.value.col, self.right.row + direction.value.row)]


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
def can_push_box_in_direction(box:Box, boxes:list[Box], walls:set[Point], move:Direction) -> bool:
    points_to_test = box.get_points_in_direction(move)

    if len(set(points_to_test).intersection(walls)) > 0:
        return False # some of these points to inspect were walls
    
    # this set filters out boxes directly above/below the current box.
    # prevents it being evaluated twice
    found_adjacent_boxes = set()
    for point_to_test in points_to_test:
        boxes_this_point_is_in = [ box for box in boxes if box.point_is_in_this_box(point_to_test)]
        if len(boxes_this_point_is_in) == 1:
            found_adjacent_boxes.add(boxes_this_point_is_in[0])

    # we now have a list of adjacent boxes to check
    if len(found_adjacent_boxes) > 0:
        # Logical AND everything together
        return all([can_push_box_in_direction(adjacent_box, boxes, walls, move) for adjacent_box in found_adjacent_boxes])
    else:
        return True # wasnt walls, wasnt boxes
    
def get_all_adjacent_boxes(box:Box, boxes:list[Box], move: Direction) -> set[Box]:
    points_to_test = box.get_points_in_direction(move)
    found_adjacent_boxes = set()
    for point_to_test in points_to_test:
        boxes_this_point_is_in = [ box for box in boxes if box.point_is_in_this_box(point_to_test)]
        if len(boxes_this_point_is_in) == 1:
            found_adjacent_boxes.add(boxes_this_point_is_in[0])

    # union all the sets together
    return set([box]).union(*[get_all_adjacent_boxes(b, boxes, move) for b in found_adjacent_boxes])

def push_box_in_direction(box:Box, boxes:list[Box], move:Direction) -> list[Box]:
    # for all boxes adjacent to this one in a direction, increase the coord in that direction
    updated_boxes = set(boxes)
    boxes_to_move = get_all_adjacent_boxes(box, boxes, move)
    # remove the boxes we will be moving from the existing set of boxes
    updated_boxes = updated_boxes.difference(boxes_to_move)
    
    for box_to_move in boxes_to_move:
        # add back in the new box points
        updated_boxes.add(Box(Point(box_to_move.left.col + move.value.col, box_to_move.left.row + move.value.row), Point(box_to_move.right.col + move.value.col, box_to_move.right.row + move.value.row)))

    return updated_boxes

def perform_single_move_if_possible(boxes: list[Box], walls: set[Point], robot_point:Point, move:Direction) -> Tuple[List[Box], Point]:
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
    adjacent_box = [ box for box in boxes if box.point_is_in_this_box(target_robot_position_point) ][0]

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
    wall_points = set(grid.get_matching_positions("#"))
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