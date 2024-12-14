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

def checksum(disk_layout):
    total = 0
    for ix, val in enumerate(disk_layout):
        if val != ".":
            total += (ix * int(val))
    return total

def solve(lines:list[str]):
    disk_layout = expand_disk_def(lines[0])

    space_ptr = 0
    file_ptr = len(disk_layout) - 1
    
    while space_ptr < file_ptr:
        # space pointer currently on a file. increment and go again.
        if disk_layout[space_ptr] != ".":
            space_ptr += 1
            continue

        # file pointer current on a space. increment and go again.
        if disk_layout[file_ptr] == ".":
            file_ptr -= 1
            continue

        # space pointer on a space. file pointer on a file
        disk_layout[space_ptr] = disk_layout[file_ptr]
        disk_layout[file_ptr] = "."

        # roll both pointers as both values used
        space_ptr += 1
        file_ptr -= 1

    print(checksum(disk_layout))
