def get_data(file):
    with open(file, 'r') as f:
        data = list(map(int,f.read().split("\n")))
    return data

def part1(depths):
  count = 0
  measurements = len(depths)
  i=0
  while i < measurements-1:
    if depths[i] < depths[i+1]:
      count +=1
    i+=1

  return count

def part2(depths):
  count = 0
  i=0
  measurements = len(depths)
  while i< measurements - 3:
    depth1 = depths[i]+depths[i+1]+depths[i+2]
    depth2 = depths[i+1]+depths[i+2]+depths[i+3]
    if depth2 >depth1:
      count+=1
    i+=1
  
  return count

depthmeasurements = get_data("Day1Data.txt")

print(part1(depthmeasurements))
print(part2(depthmeasurements))


