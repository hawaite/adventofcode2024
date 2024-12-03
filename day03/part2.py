import re

def solve(lines:list[str]):
    memory = ''.join(lines)
    instruction_matches = re.compile(r"mul\([0-9]{1,3},[0-9]{1,3}\)|do\(\)|don't\(\)").finditer(memory)

    enabled = True
    total = 0
    for instruction in instruction_matches:
        if instruction.group() == "do()":
            enabled = True
        elif instruction.group() == "don't()":
            enabled = False
        else:
            if enabled:
                parts = instruction.group()[4:-1].split(",")
                total += (int(parts[0]) * int(parts[1]))
    
    print(total)