def get_data(file):
    with open(file, 'r') as f:
        data = list(map(int,f.read().split("\n")))
    return data

data = get_data("Day10TestInput.txt")

def part_one(joltage):

  sorted_joltage = joltage
  sorted_joltage.sort()
  sorted_joltage.append(sorted_joltage[-1]+3)


  rating = 0
  one_diff_count = 0
  three_diff_count = 0

  for jolt in sorted_joltage:
    if jolt - rating == 1:
      one_diff_count += 1
      rating = jolt
    elif jolt - rating == 2:
      rating = jolt
    elif jolt - rating == 3:
      three_diff_count += 1
      rating = jolt

  return (one_diff_count*three_diff_count)

print("Part One:",part_one(data))

def part_two(index, nodes, lookup):
  result = 0
  indexes_to_visit = []

  if index not in lookup:

    for i in range(index + 1, index + 4):
      if i < len(sorted_nodes):
          if sorted_nodes[i] - sorted_nodes[index] in (1, 2, 3):
            indexes_to_visit.append(i)
      else:
          break

    if indexes_to_visit:
      for index_to_visit in indexes_to_visit:
        result += part_two(index_to_visit, sorted_nodes, lookup)
        lookup[index] = result
    else:
        return 1

  return lookup[index]

lookup = {}

sorted_nodes = data
sorted_nodes.sort()
sorted_nodes.append(sorted_nodes[-1]+3)
sorted_nodes.insert(0,0)

print("Part Two:",part_two(0,data,lookup))
