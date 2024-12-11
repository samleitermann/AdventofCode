from collections import defaultdict
def get_data(file):
    # create a list of files and empty space allocations
    with open(file) as f:
        stones = {int(x):1 for x in f.readline().split(' ')}
    return stones


def blink(stones):

    new_stones = defaultdict(int)

    for stone, count in stones.items():
        if stone == 0:
            new_stones[1] += count

        elif len(str(stone)) % 2 == 0:
            s = str(stone)
            left = s[:len(s) //2]
            right = s[len(s) //2:]
            new_stones[int(left)] += count
            new_stones[int(right)] += count
        else:
            new_stones[stone*2024] += count

    return new_stones

def solution(stones, blinks):
    part1 = stones.copy()
    for i in range(blinks):
        part1 = blink(part1)

    return sum(part1.values())


stones = get_data('real_input.txt')
result1 = solution(stones,25)
result2 = solution(stones,75)

print(f'Part 1: {result1} and Part 2: {result2}')




