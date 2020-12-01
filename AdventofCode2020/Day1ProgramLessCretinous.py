def get_data(file):
    with open(file, 'r') as f:
        data = list(map(int,f.read().split("\n")))
    return data

data = get_data("Day1Input.txt")

data = data[:]
print(data)

def aocday1pt1(exp, sum):
  expenses=exp[:]

  for expense in expenses:
      goal = sum - expense
      if goal in expenses:
          return (expense, key)


print(aocday1pt1(data))

def aocday1pt2(exp):
  expenses=exp[:]
  for i in range(0, len(expenses)):
    for j in range(i+1,len(expenses)):
      if (expenses[i]+expenses[j]) < 2020:
        for k in range(j+1, len(expenses)):
          if expenses[i]+expenses[j]+expenses[k] ==2020:
            return expenses[i]*expenses[j]*expenses[k]

#print(aocday1pt2(data))
