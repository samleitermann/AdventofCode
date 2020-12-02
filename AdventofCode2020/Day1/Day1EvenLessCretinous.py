def get_data(file):
    with open(file, 'r') as f:
        data = list(map(int,f.read().split("\n")))
    return data

data = get_data("Day1Input.txt")

print(data)

def part1(goal, input):
  for x in input:
    if (target-x in input):
      return (x, target - x)

print(part1(2020,data)[0]*part1(2020,data)[0])