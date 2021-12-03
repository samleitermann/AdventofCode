# ---Opening Data---
# Open data and strip out newlines

def get_data(file):
    with open(file, encoding='utf-8') as f:
        data = f.read()
        inputs = data.splitlines()
    return inputs



# ---Fetching Data and Defining Variables---
# fetch data and initialize passport array, define fields and
direction_input = get_data("Day2Data.txt")

directions = []


# ---Taking List to Dict---

for index, i in enumerate(direction_input):
    rawdata = i.split()
    rawdata[1] = int(rawdata[1])
    directions.append(rawdata)

#Part One Solution#
def part_one(directions):
  horizontal = 0
  vertical = 0
  #Simply checks the instruction and then increases the appropriate value#
  for dir in directions:
    if dir[0] == 'forward':
      horizontal += dir[1]
    if dir[0] == 'down':
      vertical += dir[1]
    if dir[0] == 'up':
      vertical -= dir[1]
  
  return horizontal*vertical

print(part_one(directions))

def part_two(directions):
  horizontal = 0
  vertical = 0
  aim = 0
  #Similar to part one, except the instructions mean something different#
  for dir in directions:
    if dir[0] == 'forward':
      horizontal += dir[1]
      vertical += aim*dir[1]
    if dir[0] == 'down':
      aim += dir[1]
    if dir[0] == 'up':
      aim -= dir[1]
  
  return horizontal*vertical

print(part_two(directions))
