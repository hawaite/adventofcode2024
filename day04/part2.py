class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return "(%d,%d)" % (self.x,self.y)

    def inside_bounds(self, width, height):
        return not (self.x < 0 or self.x >= width or self.y < 0 or self.y >= height)

def get_x_centered_at_point(center):
    span_one = [Point(center.x-1, center.y-1), Point(center.x, center.y), Point(center.x+1, center.y+1)] #top left to bottom right
    span_two = [Point(center.x+1, center.y-1), Point(center.x, center.y), Point(center.x-1, center.y+1)] #top right to bottom left
    return (span_one, span_two)

def all_points_in_bounds(cross, width, height):
    return all([x.inside_bounds(width,height) for x in cross[0]]) and all([x.inside_bounds(width,height) for x in cross[1]])

def points_spell_mas_either_direction(points_list, crossword):
    return "".join([crossword[point.y][point.x] for point in points_list]) in ["MAS","SAM"]

def is_x_mas_in_any_orientation(point,width,height, crossword):
    if crossword[point.y][point.x] != "A": # early escape
        return False
    
    cross_points = get_x_centered_at_point(point)
    if not all_points_in_bounds(cross_points, width, height):
        return False
    
    return points_spell_mas_either_direction(cross_points[0], crossword) and points_spell_mas_either_direction(cross_points[1], crossword)
    

def solve(lines:list[str]):
    width = len(lines[0])
    height = len(lines)
    total = 0
    for row in range(0,len(lines)):
        for col in range(0, len(lines[0])):
            is_valid = is_x_mas_in_any_orientation(Point(col,row),width,height,lines)
            if is_valid:
                total += 1

    print(total)