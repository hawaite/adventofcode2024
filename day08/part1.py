from util.grids import GridUtil, Point
from itertools import combinations

def solve(lines:list[str]):
    # initialize a dict with all the signal types as keys and empty lists as starting vals
    signals = {key: [] for key in set("".join(lines)).difference(set("."))}
    antinodes = set() # antinodes from different signals count as the same

    width = len(lines[0])
    height = len(lines)

    all_antenna = GridUtil.get_positions_matching_from_lines(lines, lambda char: (char != "."))
    for antenna_location in all_antenna:
        signal_type = lines[antenna_location.row][antenna_location.col]
        signals[signal_type].append(antenna_location)
    print(signals)

    for signal in signals.keys():
        signal_antennas = signals[signal]
        antenna_combinations = list(combinations(signal_antennas, 2))
        # get horizontal difference
        for pair in antenna_combinations:
            horizontal_distance = pair[0].col - pair[1].col
            vertical_distance = pair[0].row - pair[1].row
            antinode_one = Point(pair[0].col + horizontal_distance, pair[0].row + vertical_distance)

            # flip signs on distances
            antinode_two = Point(pair[1].col + (horizontal_distance * -1), pair[1].row + (vertical_distance * -1))

            if GridUtil.position_in_bounds(antinode_one, width, height):
                antinodes.add(antinode_one)

            if GridUtil.position_in_bounds(antinode_two, width, height):
                antinodes.add(antinode_two)

    print(len(antinodes))