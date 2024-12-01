import os

def solve(lines:list[str]):
    locations_list_left = []
    right_side_counts = {}

    for line in lines:
        parts = line.split("   ")
        locations_list_left.append(int(parts[0]))
        if int(parts[1]) not in right_side_counts.keys():
            right_side_counts[int(parts[1])] = 0

        right_side_counts[int(parts[1])] = right_side_counts[int(parts[1])] + 1

    scores = [ (0 if x not in right_side_counts.keys() else x * right_side_counts[x]) 
         for x in locations_list_left]

    print(sum(scores))

def main():
    cwd = os.path.dirname(__file__)

    with(open(f"{cwd}/input.txt", 'r') as fp):
        all_lines = fp.readlines()

    all_lines_stripped = [line.strip() for line in all_lines]

    solve(all_lines_stripped)

if __name__ == "__main__":
    main()