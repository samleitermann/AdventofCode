from collections import namedtuple
import re

def parse_raw(file):

    raw_data = []

    # open the file and strip out trailing whitespace

    with open(file, 'r') as f:
        str_inp = f.readline()

    list_inp = str_inp.split(",")

    for line in list_inp:
        current_range = line.split("-")
        raw_data.append((int(current_range[0]), int(current_range[1])))
    return raw_data

data = parse_raw("real_input.txt")
print(data)

# providing this default is somewhat of a hack - there isn't any other way to
# force type inference to happen, AFAIK - but this won't work with standard
# collections (list, set, dict, tuple)

def is_repeating(number_str, part):

    if len(number_str) == 2 and number_str[0] == number_str[1]:
        return True
    else:
        pattern = r"^(\d+)\1+$"
        pattern_2 = r"^(\d+)\1$"
        if part == 1:
            return bool(re.match(pattern, number_str))
        if part == 2:
            return bool(re.match(pattern_2, number_str))


def part_one(data=data):
    bad_ids = []

    for row in data:
        for i in range(row[0], row[1] + 1):
            if is_repeating(str(i), 1):
                bad_ids.append(i)


    return sum(bad_ids)

print(part_one(data))



#aoc_helper.lazy_test(day=1, year=2025, parse=parse_raw, solution=part_one)


# providing this default is somewhat of a hack - there isn't any other way to
# force type inference to happen, AFAIK - but this won't work with standard
# collections (list, set, dict, tuple)
def part_two(data=data):
    bad_ids = []

    for row in data:
        for i in range(row[0], row[1] + 1):

            if is_repeating(str(i), 2):
                bad_ids.append(i)

    return sum(bad_ids)

