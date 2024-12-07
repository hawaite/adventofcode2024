def ternary(n):
    if n == 0:
        return '0'
    nums = []
    while n:
        n, r = divmod(n, 3)
        nums.append(str(r))
    return ''.join(reversed(nums))

def could_be_valid(target:int, components:list[int]) -> bool:
    for i in range(0,pow(3,len(components)-1)):
        # 0 wil represnt "add" and 1 will represent "multiply" and 2 will represent concat
        add_mult_cat_ordering = ternary(i)
        add_mult_cat_ordering = add_mult_cat_ordering.zfill(len(components)-1)

        running_total = components[0]
        for n in range(1, len(components)): # running total always starts with the first element
            operator = add_mult_cat_ordering[n-1]
            if operator == "0": #add
                running_total += components[n]
            elif operator == "1": #mult
                running_total *= components[n]
            else: #concat
                running_total = int(str(running_total) + str(components[n]))

        if running_total == target:
            return True
    return False


def solve(lines:list[str]):
    total = 0

    for line in lines:
        parts = line.split(": ")
        target = int(parts[0])
        components = [int(x) for x in parts[1].split(" ")]

        if could_be_valid(target, components):
                total += target
        

    print(total)