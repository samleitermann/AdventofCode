def get_data(file):
    with open(file, 'r') as f:
        data = list(map(int,f.read().split("\n")))
    return data

def part1(depths):
  count = 0
  measurements = len(depths)=1
  while i< measurements:
    if depth[i] > depth[i+1]:
      count +=1
    i+=1

  return count

depthmeasurements = get_data("Day1Data.txt")

print(depthmeasurements)

