import os

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

def main():
    cwd = os.path.dirname(__file__)

    with(open(f"{cwd}/example.txt", 'r') as fp):
        all_lines = fp.readlines()

    all_lines_stripped = [line.strip() for line in all_lines]

    solve(all_lines_stripped)

if __name__ == "__main__":
    main()