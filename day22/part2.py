from collections import deque
from itertools import product
big_dumb_list_of_combinations = list(product([-9,-8,-7,-6,-5,-4,-3,-2,-1,0,1,2,3,4,5,6,7,8,9],[-9,-8,-7,-6,-5,-4,-3,-2,-1,0,1,2,3,4,5,6,7,8,9], [-9,-8,-7,-6,-5,-4,-3,-2,-1,0,1,2,3,4,5,6,7,8,9], [-9,-8,-7,-6,-5,-4,-3,-2,-1,0,1,2,3,4,5,6,7,8,9]))

def get_banana_sales(starting_number, max_times, trigger_combination:list[int]):
    secret_number = int(starting_number)
    changes = deque([], maxlen=4)
    final_digit = secret_number % 10
    for _ in range(0,max_times):
        # step 1
        temp = secret_number * 64
        secret_number = secret_number ^ temp # mix is XOR
        secret_number = secret_number % 16777216 # prune is modulo 16777216

        # step 2
        temp = int(secret_number / 32)
        secret_number = secret_number ^ temp
        secret_number = secret_number % 16777216

        # step 3
        temp = secret_number * 2048
        secret_number = secret_number ^ temp
        secret_number = secret_number % 16777216

        # get the final digit
        new_final_digit = secret_number % 10
        change = new_final_digit - final_digit
        changes.append(change)
        # print(changes)
        if list(changes) == trigger_combination:
            # print("matched passed trigger")
            return new_final_digit
        final_digit = new_final_digit
        
    return 0

def prune_studid_combination_list(combination_list):
    # there are combinations that are obviously not possible
    # simple prune anything that goes outside of +/-9 when starting from 0
    new_combination_list = []
    for combo in combination_list:
        combo_list = list(combo)
        
        test_num = 0
        valid = True
        for num in combo_list:
            test_num += num
            if test_num < -9 or test_num > 9:
                valid = False
                break
        if valid:
            new_combination_list.append(combo)

    return new_combination_list


def solve(lines:list[str]):
    best_combination = []
    best_combination_count = 0

    # print(len(big_dumb_list_of_combinations))
    # print(len(prune_studid_combination_list(big_dumb_list_of_combinations)))

    for trigger_combination in prune_studid_combination_list(big_dumb_list_of_combinations):
        total = 0
        for line in lines:
            received_bananas = get_banana_sales(line, 2000, list(trigger_combination))
            total += received_bananas

        if total > best_combination_count:
            print(f"new best!: {trigger_combination} - {total}")
            best_combination_count = total
            best_combination = trigger_combination

    print(f"best count {best_combination_count}")
    print(f"combination: {best_combination}")