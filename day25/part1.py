def parse_lock_or_key(lock_or_key_line_buffer):
    lock_or_key_def = []
    for col in range(0, len(lock_or_key_line_buffer[0])):
        col_total = 0
        for row in range(0,len(lock_or_key_line_buffer)):
            if lock_or_key_line_buffer[row][col] == "#":
                col_total+= 1
        lock_or_key_def.append(col_total-1)
    return lock_or_key_def

def solve(lines:list[str]):
    keys = []
    locks = []
    lock_or_key_line_buffer = []
    for line in lines:
        if line == "":
            # finished fetching a lock or key def
            if lock_or_key_line_buffer[0] == "#####": #lock
                locks.append(parse_lock_or_key(lock_or_key_line_buffer))
            else: # key
                keys.append(parse_lock_or_key(lock_or_key_line_buffer))
            lock_or_key_line_buffer = []
        else:
            lock_or_key_line_buffer.append(line)

    valid_combos = 0
    # a key + lock combo is valid if it does not overlap.
    # this means we just need to check that summing the columns does not exceed 5 '#' symbols
    # no need to check for EXACT matches.
    for key in keys:
        for lock in locks:
            all_less_than_five = [x for x in [x + y for x, y in zip(key, lock)] if x <=5]
            if len(all_less_than_five) == 5:
                valid_combos += 1
    print(valid_combos)