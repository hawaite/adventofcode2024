from util.grids import GridUtil, Point
from itertools import combinations

def solve(lines:list[str]):
    signals = {key: [] for key in set("".join(lines)).difference(set("."))}
    antinodes = set() # antinodes from different signals count as the same

    width = len(lines[0])
    height = len(lines)

    all_antenna = GridUtil.get_positions_matching_from_lines(lines, lambda char: (char != "."))
    for antenna_location in all_antenna:
        signal_type = lines[antenna_location.row][antenna_location.col]
        signals[signal_type].append(antenna_location)

    # for part 2, a signal consisting of more than one antenna will have all the antennas as antinodes
    # signals with only 1 antenna will not necessarily have itself as an antinode
    for signal,antennas in signals.items():
        if len(antennas) != 1:
            antinodes = antinodes.union(antennas)            

    for signal in signals.keys():
        signal_antennas = signals[signal]
        # iterate over every combination of antennas in that signal 
        antenna_combinations = list(combinations(signal_antennas, 2))

        for pair in antenna_combinations:
            horizontal_distance = pair[0].col - pair[1].col
            vertical_distance = pair[0].row - pair[1].row

            pos_to_test = pair[0]
            # keep adding and testing nodes in a given direction
            while True:
                antinode = Point(pos_to_test.col + horizontal_distance, pos_to_test.row + vertical_distance)
                if GridUtil.position_in_bounds(antinode, width, height):
                    antinodes.add(antinode)
                    pos_to_test = antinode
                else:
                    break

            pos_to_test = pair[1]
            while True:
                # flip signs on distances
                # keep adding and testing nodes in opposite direction direction
                antinode = Point(pos_to_test.col + (horizontal_distance * -1), pos_to_test.row + (vertical_distance * -1))
                if GridUtil.position_in_bounds(antinode, width, height):
                    antinodes.add(antinode)
                    pos_to_test = antinode
                else:
                    break

    print(len(antinodes))
