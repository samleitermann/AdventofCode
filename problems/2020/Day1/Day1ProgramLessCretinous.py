def get_data(file):
    with open(file, 'r') as f:
        data = list(map(int,f.read().split("\n")))
    return data

data = get_data("Day1Input.txt")
data = data[:]


def aocday1pt1(exp, sum):
  expenses=exp[:]

  for expense in expenses:
      goal = sum - expense
      if goal in expenses:
          return (expense, goal)
  return -1


print(aocday1pt1(data,2020)[0]*aocday1pt1(data,2020)[1] )

def aocday1pt2(exp, sum):
  expenses=exp[:]

  for expense in expenses:
      remainder = sum - expense
      pair = aocday1pt1(exp, remainder)

      if pair != -1 and pair [0] != pair[1] and expense not in pair:
          return (expense, pair[0], pair[1])
  return -1

print(aocday1pt2(data,2020)[0]*aocday1pt2(data,2020)[1]*aocday1pt2(data,2020)[2])
