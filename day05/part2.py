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

# takes an update and a rule. If the rule applies, and the rule is broken, 
# then swap the two offending indexes to make the rule valid
def apply_rule_once_inplace(update:list[int], rule):
    if (rule[0] not in update) or (rule[1] not in update): # both numbers need to be present to make sense
        return update # rule does not apply to this update
    
    if rule_is_broken(update, rule):
        ix_of_earlier = update.index(rule[0])
        ix_of_later = update.index(rule[1])
        # swap values in list
        temp = update[ix_of_earlier]
        update[ix_of_earlier] = update[ix_of_later]
        update[ix_of_later] = temp
        
# takes the update list, and the rules list, and actions every rule until the update is valid
def fix_inplace(update, rules):
    while not is_valid(update,rules):
        for rule in rules:
            apply_rule_once_inplace(update, rule)

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
        if not is_valid(update, rules):
            fix_inplace(update, rules)
            middle_index = math.floor(len(update) / 2)
            total += update[middle_index]

    print(total)