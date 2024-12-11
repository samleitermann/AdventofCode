def get_data(file):
    with open(file, 'r') as f:
        data = list(map(int,f.read().split("\n")))
    return data

data = get_data(C:\Users\samle\OneDrive\Documents\GitHub\AdventofCode\AdventofCode2020\Day1\Day1Input.txt)

print(data)

def part1(goal, expense):
  for x in expense:
    if (goal-x in expense):
      return (x, goal - x)

print(part1(2020,data)[0]*part1(2020,data)[1])

def part2(goal, expense):
  for x in expense:
    for y in expense:
      if (goal-x-y in expense):
        return (x, y, goal-x-y)

print(part2(2020,data)[0]*part2(2020,data)[1]*part2(2020,data)[2])
