import re

def get_data(file):
  data=[]
  with open(file, 'r') as f:

     instructions = f.read().split('\n\n')
  return instructions

def part_one(instructions):

    seeds = re.findall(r'(\d+)',instructions[0])

    min_location = float('inf')

    for seed in map(int,seeds):
        for inst in instructions[1:]:
            for correspondence in re.findall(r'(\d+) (\d+) (\d+)',inst):
                destination, start, delta = map(int, correspondence)
                if seed in range(start,start+delta):
                    seed += destination-start
                    break

        min_location = min(seed,min_location)

    return min_location

print(part_one(get_data('Day5Input.txt')))

def part_two(instructions):

    seed_intervals = []

    for seed in re.findall(r'(\d+) (\d+)',instructions[0]):
        x1, dx = map(int,seed)
        x2 = x1+dx
        seed_intervals.append((x1,x2,1))

    min_location = float('inf')

    while seed_intervals:




    return seed_intervals

print(part_two(get_data('Day5Input.txt')))







