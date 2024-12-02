def solve(lines:list[str]):
    locations_list_left = []
    locations_list_right = []
    for line in lines:
        parts = line.split("   ")
        locations_list_left.append(int(parts[0]))
        locations_list_right.append(int(parts[1]))

    zipped_and_sorted = zip(sorted(locations_list_left), sorted(locations_list_right))
    distances = [abs(pair[0] - pair[1]) for pair in zipped_and_sorted]
    print(sum(distances))