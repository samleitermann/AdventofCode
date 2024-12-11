# ---Opening Data---
# Open data and strip out newlines

def get_data(file):
    with open(file, encoding='utf-8') as f:
        data = f.read()
        inputs = data.split('\n')
    return inputs


rules = get_data("Day7Input.txt")


def part_one(bags, whichbag):
    ListOfBags = []
    for bag in bags:
        BagFind = bag.find(" bags contain")
        if whichbag in bag[BagFind:]:
            ListOfBags.append(bag[:BagFind])
            ListOfBags.extend(part_one(bags, bag[:BagFind]))
    return ListOfBags


print("Part One:", len(set(part_one(rules, "shiny gold"))))

AllTheBags = {}

for rule in rules:
    rule = rule.replace("bags", "").replace("bag", "").strip(".")
    rule = rule.split("contain")
    AllTheBags[rule[0].strip()] = rule[1].strip().split(",")

temp = AllTheBags['plaid olive']


def getBags(bags):
    total = 1

    if "no other" in AllTheBags[bags]:
        return 1
    for colors in AllTheBags[bags]:
        each = colors.split()
        total += int(each[0]) * getBags(" ".join(each[1:]))
    return total


print("Part One:", getBags("shiny gold") - 1)
