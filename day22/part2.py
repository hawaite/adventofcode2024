def generate_digit_list(starting_number, times):
    last_digit_numbers = [ starting_number % 10 ]
    secret_number = int(starting_number)
    for _ in range(0,times-1):
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
        last_digit_numbers.append(secret_number % 10)
    return last_digit_numbers

def generate_difference_list(digit_list):
    diff_list = []
    for _, diff_window in window(digit_list, 2):
        diff_list.append(diff_window[0] - diff_window[1])

    return diff_list

# returns a dictionary of all the trigger values to the number of bananas returned 
def get_banana_sales_value(starting_number, times):
    digits = generate_digit_list(starting_number, times)
    diff_list = generate_difference_list(digits)

    result_dict = {}
    for i, diff_window in window(diff_list, 4):
        # turn the list in to a tuple because tuples are hashable, while lists are not
        if tuple(diff_window) not in result_dict.keys():
            result_dict[tuple(diff_window)] = digits[i+4]

    return result_dict

def window(lst:list, size:int):
    for i in range(0, len(lst) - size + 1):
        yield (i, lst[i:i+size])

def solve(lines:list[str]):
    pattern_counts = {}
    for line in lines:
        seller_patterns = get_banana_sales_value(int(line), 2000)
        for k,v in seller_patterns.items():
            if k not in pattern_counts.keys():
                pattern_counts[k] = 0
            pattern_counts[k] = pattern_counts[k] + v

    best_combination = None
    best_combination_count = 0

    for k,v in pattern_counts.items():
        if v > best_combination_count:
            best_combination = k
            best_combination_count = v
    
    print(f"best count {best_combination_count}")
    print(f"combination: {best_combination}")