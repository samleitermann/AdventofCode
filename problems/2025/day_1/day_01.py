from collections import Counter, defaultdict, deque

import aoc_helper
from aoc_helper import (
    Grid,
    PrioQueue,
    SparseGrid,
    decode_text,
    extract_ints,
    extract_iranges,
    extract_ranges,
    extract_uints,
    frange,
    irange,
    iter,
    list,
    map,
    multirange,
    range,
    search,
    tail_call,
)

raw = aoc_helper.fetch(1, 2025)


def parse_raw(file):

    raw_data = []

    # open the file and strip out trailing whitespace

    with open(file, 'r') as f:
        for line in f:
            line.rstrip()
            temp1 = line[0]
            temp2 = int(line[1:].strip())

            raw_data.append((temp1, temp2))

    return raw_data

data = parse_raw("input.txt")


# providing this default is somewhat of a hack - there isn't any other way to
# force type inference to happen, AFAIK - but this won't work with standard
# collections (list, set, dict, tuple)
def part_one(data=data):
    loc = 50
    count = 0
    for instr in data:
        if instr[0] == "L":
            loc = (loc - instr[1]) % 100
            if loc == 0:
                count += 1

        elif instr[0] == "R":
            loc = (loc + instr[1]) % 100
            if loc == 0:
                count += 1

    return count




#aoc_helper.lazy_test(day=1, year=2025, parse=parse_raw, solution=part_one)


# providing this default is somewhat of a hack - there isn't any other way to
# force type inference to happen, AFAIK - but this won't work with standard
# collections (list, set, dict, tuple)
def part_two(data=data):
    count = 0
    loc = 50
    #Code just counts how many rotations there are and adds those on.
    for instr in data:

        if instr[0] == "R":
            dist_to_0 = (100 - loc) % 100
            loc = (loc +  instr[1]) % 100
        else:
            dist_to_0 = loc % 100
            loc = (loc - instr[1]) % 100

        if dist_to_0 == 0:
            dist_to_0 = 100
        if instr[1] >= dist_to_0:
            count += 1 + (instr[1] - dist_to_0) // 100

    return count

