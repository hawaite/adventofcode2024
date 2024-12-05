import math

def rule_is_broken(update, rule):
    if rule[0] in update and rule[1] in update:
        ix_of_earlier = update.index(rule[0])
        ix_of_later = update.index(rule[1])
        if ix_of_later < ix_of_earlier:
            return True
    return False

def is_valid(update, rules):
    for rule in rules:
        if rule_is_broken(update, rule):
            return False
    return True

def solve(lines:list[str]):
    parse_rules = True
    rules = []
    updates = []
    for line in lines:
        if line == "":
            parse_rules = False
            continue
        if parse_rules == True:
            parts = line.split("|")
            rules.append((int(parts[0]),int(parts[1])))
        else:
            update = [int(x) for x in line.split(",")]
            updates.append(update)

    total = 0
    for update in updates:
        update_is_valid = is_valid(update, rules)

        if update_is_valid:
            middle_index = math.floor(len(update) / 2)
            total += update[middle_index]

    print(total)