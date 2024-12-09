#takes a disk definition and fully expands it.
def expand_disk_def(disk_def):
    digits = [int(x) for x in list(disk_def)]
    is_free_space = False
    expanded_disk_def_parts = []
    file_id = 0
    for i in range(0, len(digits)):
        if is_free_space:
            expanded_disk_def_parts.extend("."*digits[i])
        else:
            for j in range(0,digits[i]):
                expanded_disk_def_parts.append(str(file_id))
            file_id += 1
        is_free_space = not is_free_space
    return expanded_disk_def_parts

def find_all_space_ordered(disk_def):
    found_spaces = []

    for ix, val in enumerate(disk_def):
        if val == ".":
            found_spaces.append(ix)
    return found_spaces

def checksum(disk_layout):
    total = 0
    for ix, val in enumerate(disk_layout):
        if val != ".":
            total += (ix * int(val))
    return total
def solve(lines:list[str]):
    disk_layout = expand_disk_def(lines[0])

    free_spaces = find_all_space_ordered(disk_layout)
    for i in range(0,len(disk_layout)):
        ix_item_to_move = len(disk_layout) -1 - i
        if disk_layout[ix_item_to_move] == ".":
            continue
        else:
            ix_earliest_free_space = free_spaces[0]
            free_spaces = free_spaces[1:]
            if ix_earliest_free_space > ix_item_to_move:
                break # everything beyond here is free space
            disk_layout[ix_earliest_free_space] = disk_layout[ix_item_to_move]
            disk_layout[ix_item_to_move] = "."

    print(checksum(disk_layout))