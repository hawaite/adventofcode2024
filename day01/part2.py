from collections import defaultdict

def solve(lines:list[str]):
    locations_list_left = []
    right_side_counts = defaultdict(int)

    for line in lines:
        parts = line.split("   ")
        locations_list_left.append(int(parts[0]))

        right_side_counts[int(parts[1])] = right_side_counts[int(parts[1])] + 1

    scores = [ (0 if x not in right_side_counts.keys() else x * right_side_counts[x]) 
         for x in locations_list_left]

    print(sum(scores))