import re

def solve(lines:list[str]):
    memory = ''.join(lines)
    instruction_matches = re.finditer(r"mul\([0-9]{1,3},[0-9]{1,3}\)", memory)
    parts_list = [ x.group()[4:-1].split(",") for x in instruction_matches]
    total = sum([int(x[0]) * int(x[1]) for x in parts_list])
    
    print(total)