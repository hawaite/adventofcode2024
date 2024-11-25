import os
import shutil
import requests
import sys
from enum import Enum

class ExitStatus(Enum):
    EXIT_BAD_CLI_ARGS = 1
    EXIT_NO_SESSION_TOKEN = 2
    EXIT_INPUT_FETCH_FAIL = 3


session_token_environment_var = "AOC_SESSION_TOKEN"
day_input_url = "https://adventofcode.com/2024/day/%s/input"

# fetches the problem input and creates a new directory to hold the solution in the current directory
def main():
    if (len(sys.argv) != 2) or (not sys.argv[1].isnumeric()):
        print("usage: python init_day.py <day number>")
        exit(ExitStatus.EXIT_BAD_CLI_ARGS.value)

    session_token = os.environ.get(session_token_environment_var)
    
    day = int(sys.argv[1])
    day_zero_padded = "%02d" % day
    day_path = "day%s" % day_zero_padded

    if not session_token:
        print("AOC_SESSION_TOKEN not set")
        exit(ExitStatus.EXIT_NO_SESSION_TOKEN.value)
        
    res = requests.get(day_input_url % day, cookies={"session": session_token})

    if not res.ok:
        print("fetch failed with reason: %s" % res.reason)
        exit(ExitStatus.EXIT_INPUT_FETCH_FAIL.value)

    project_root = os.path.dirname(__file__)
    day_root = os.path.join(project_root, day_path)

    if not os.path.exists(day_root) :
        print("creating %s" % day_root)
        os.mkdir(day_root)

    # unconditionally overwrite input file
    with open(os.path.join(day_root, "input.txt"), mode="w") as fp:
        print("writing %s" % os.path.join(day_root, "input.txt"))
        fp.write(res.text)

    # only create template solution files if one doesnt already exist
    part_one_path = os.path.join(day_root, "part1.py")
    if not os.path.exists(part_one_path):
        print("writing default %s" % part_one_path)
        shutil.copy(os.path.join(project_root, "template.py"), part_one_path)

    part_two_path = os.path.join(day_root, "part2.py")
    if not os.path.exists(part_two_path):
        print("writing default %s" % part_two_path)
        shutil.copy(os.path.join(project_root, "template.py"), part_two_path)

if __name__ == "__main__":
    main()