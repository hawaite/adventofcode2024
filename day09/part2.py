from dataclasses import dataclass
from collections import deque
from typing import Dict, Tuple

@dataclass
class Span:
    start: int
    length:int

#takes a disk definition and fully expands it.
def get_files_and_spaces(disk_def) -> Tuple[Dict[str, Span], list[Span]]:
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

def checksum_from_file_dict(file_dict:Dict[str, Span]):
    total = 0
    for file_id, file_span in file_dict.items():
        for i in range(file_span.start, file_span.start + file_span.length):
            total += (i * file_id)
    return total

# this will order the remaining space and consolidate contiguous blocks of space in to a single space
def order_and_consolidate_space(spaces:list[Span]) -> list[Span]:
    sorted_spaces = sorted(spaces, key=lambda space_span : space_span.start) 
    i = 0
    while True:
        if i == len(sorted_spaces) - 1:
            break # at last element, meaning cant get an i+1
        space_one = sorted_spaces[i]
        space_two = sorted_spaces[i+1]
        if space_one.start + space_one.length == space_two.start:
            # these two can be combined
            # update the first one and delete the second one
            space_one.length = space_one.length + space_two.length
            del sorted_spaces[i+1]
            # dont increment i. the new value at i may be combinable with i + 1
        else:
            # cant combine these two so move on
            i += 1

    return sorted_spaces

def solve(lines:list[str]):
    files, spaces = get_files_and_spaces(lines[0])
    file_keys = deque(files.keys())

    while len(file_keys) > 0:
        file = files[file_keys.pop()]
        # iterate all spaces to see if theres somewhere that works
        for space in spaces:
            if space.start > file.start:
                break # bail if space is later than the original space

            if space.length == file.length:
                original_file_start = file.start
                file.start = space.start
                space.start = original_file_start
                spaces = order_and_consolidate_space(spaces)
                break # file moved.
            elif space.length > file.length:
                # space bigger than file.
                original_file_start = file.start
                # place file in space
                file.start = space.start
                # reduce space that was there and shuffle it to end of what was just added
                space.start = space.start + file.length
                space.length = space.length - file.length

                # add new space where the file used to be
                new_space = Span(original_file_start, file.length)
                spaces.append(new_space)
                spaces = order_and_consolidate_space(spaces)
                break # file moved

    print(checksum_from_file_dict(files))