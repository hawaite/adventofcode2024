def iterate_number(starting_number, times):
    secret_number = int(starting_number)
    for i in range(0,times):
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

    return secret_number

def solve(lines:list[str]):
    total = 0
    for line in lines:
        iterated_number = iterate_number(line, 2000)
        total += iterated_number
        # print(f"{line} - {iterated_number}")

    print(f"total: {total}")