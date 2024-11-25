import os

def solve(lines:list[str]):
    pass

def main():
    cwd = os.path.dirname(__file__)

    with(open(f"{cwd}/input.txt", 'r') as fp):
        all_lines = fp.readlines()

    all_lines_stripped = [line.strip() for line in all_lines]

    solve(all_lines_stripped)

if __name__ == "__main__":
    main()