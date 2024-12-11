def get_data(file):
  data=[]
  with open(file, 'r') as f:
     for line in f:
       data.append(line)
  return data



rawdata=get_data("Day11Data.txt")

def partone(rawdata):
  
  elves = []
  calories=[]
  elf=[]
  
  for item in rawdata:
    if item != '\n':
      elf.append(int(item))
    if item == '\n':
      elves.append(elf)
      elf = []
  
  for elf in elves:
    calories.append(sum(elf))

  return max(calories)

def parttwo(rawdata):
  
  elves = []
  calories=[]
  elf=[]
  maxes = []
  
  for item in rawdata:
    if item != '\n':
      elf.append(int(item))
    if item == '\n':
      elves.append(elf)
      elf = []
  
  for elf in elves:
    calories.append(sum(elf))

  for i in range(3):
    maxes.append(max(calories))
    calories.remove(max(calories))

    

  return sum(maxes)

print(parttwo(rawdata))    