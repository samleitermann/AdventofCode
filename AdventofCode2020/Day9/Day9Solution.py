def get_data(file):
    with open(file, 'r') as f:
        data = list(map(int, f.read().split("\n")))
    return data

data = get_data("Day9Input.txt")


def part_one(cipher):

    for i in range(len(cipher)):
        preamble = cipher[(0 + i):25 + i]
        target = cipher[25 + i]

        for pre in preamble:
            if target - pre in preamble:
                target_found = True
                break
            elif target - pre not in preamble:
                target_found = False

        if target_found == False:
            return target


def part_two(cipher, target):

    for length in range(2, len(cipher)):
        for i in range(len(cipher) - length):
            if sum(cipher[i:i + length]) == target:
                return min(cipher[i:i + length]) + max(cipher[i:i + length])


print("Part One:", part_one(data))
print("Part Two", part_two(data, part_one(data)))
