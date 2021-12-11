from collections import defaultdict as dd

octopuses = dd(int)
steps = 5000

with open("Day11Data.txt", 'r') as file:
  row = 0
  for line in file:
      column = 0
      line = line.strip()
      for character in line:
          octopuses[(row, column)] = int(character)
          column += 1
      row += 1

def get_neighbours(octos,oct):
  x,y = oct
  res = []

  for a,b in [(x-1,y),(x-1,y+1),(x-1,y-1),(x,y+1),(x,y-1),(x+1,y),(x+1,y+1),(x+1,y-1)]:
    if (a,b) in octos:
      res.append((a,b))

  return res

flashes = 0
flashtime = 9

for step in range(steps):
  for key in octopuses.keys():
    octopuses[key] +=1
  
  is_changing = True
  flashing = 0

  while is_changing:
    changes = dd(int)

    for key,value in octopuses.items():
      if value > 9:
        neighs = get_neighbours(octopuses,key)
        for neigh in neighs:
          if octopuses[neigh] == 0 or octopuses[neigh] > flashtime:
            continue
          changes[neigh] +=1
        octopuses[key] = 0
        flashing += 1
        flashes += 1
    for key in changes.keys():
      octopuses[key] = min(octopuses[key] + changes[key], flashtime+1)
    
    is_changing = len(changes) > 0

  if step == 99:
        print(f"Number of flashes until step 100 is {flashes}!")
  if flashing == len(octopuses):
      print(f"All flashed in step {step+1}!")
      break