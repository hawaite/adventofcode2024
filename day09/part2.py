from dataclasses import dataclass

@dataclass
class Span:
    start: int
    length:int

#takes a disk definition and fully expands it.
def expand_disk_def_list(disk_def):
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

#takes a disk definition and fully expands it.
def get_files_and_spaces(disk_def):
    digits = [int(x) for x in list(disk_def)]
    is_free_space = False
    files = {}
    spaces = []
    file_id = 0
    ix = 0
    for i in range(0, len(digits)):
        if is_free_space:
            if digits[i] != 0: # ignore spaces of size zero
                spaces.append(Span(ix, digits[i]))
            ix += digits[i]
        else:
            files[file_id] = Span(ix, digits[i])
            file_id += 1
            ix += digits[i]
        is_free_space = not is_free_space
    return (files, spaces)

def checksum(disk_layout):
    total = 0
    for ix, val in enumerate(disk_layout):
        if val != ".":
            total += (ix * int(val))
    return total

def solve(lines:list[str]):
    disk_layout = expand_disk_def_list(lines[0])
    print(disk_layout)
    files, spaces = get_files_and_spaces(lines[0])
    print(f"files: {files}")
    print(f"spaces: {spaces}")

    file_id_lst = list(reversed(files.keys()))
    total_files = len(file_id_lst)
    for file_id in list(reversed(files.keys())):
        print(f"{file_id} / {total_files}")
        index_to_inspect = 0
        while index_to_inspect < files[file_id].start: #only check locations before current position
            if disk_layout[index_to_inspect:index_to_inspect+files[file_id].length] == list("." * files[file_id].length):
                # move to new location
                for i in range(index_to_inspect, index_to_inspect+files[file_id].length):
                    disk_layout[i] = file_id
                #overwrite old location
                for i in range(files[file_id].start, files[file_id].start+files[file_id].length):
                    disk_layout[i] = "."
                break # can place thing here and start next file
            index_to_inspect += 1
        # print(f"after: {disk_layout}")

    # print(f"final layout: {disk_layout}")

    print(checksum(disk_layout))