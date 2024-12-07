def could_be_valid(target:int, components:list[int]) -> bool:
    for i in range(0,pow(2,len(components)-1)):
        # 0 wil represnt "add" and 1 will represent "multiply"
        add_mult_ordering = "{0:b}".format(i)
        # zero pad so always the number of operators we need
        add_mult_ordering = add_mult_ordering.zfill(len(components)-1)

        running_total = components[0] # running total always starts with the first element
        for n in range(1, len(components)):
            operator = add_mult_ordering[n-1]
            if operator == "0": #add
                running_total += components[n]
            else: #mult
                running_total *= components[n]

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