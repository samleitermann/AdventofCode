def get_data(file):
  
  with open(file, 'r') as f:
    elves = []
    for line in f:
      elf1 = []
      elf2 = []
      
      elfa,elfb = line.rstrip().split(',')
      
      elf11,elf12 = elfa.split('-')
      elf21,elf22 = elfb.split('-')

      elf1.append(int(elf11))
      elf1.append(int(elf12))

      elf2.append(int(elf21))
      elf2.append(int(elf22))

      elves.append([elf1,elf2])

  return elves

def partone(rawdata):

  count = 0

  for pair in rawdata:

    (a,b) = (pair[0][0],pair[0][1])
    (c,d) = (pair[1][0],pair[1][1])

    if (a > c) or (a == c and d > b):
      a, b, c, d = c, d, a , b

    if a <=c and b >=d:
      count +=1

  return count

print(partone(get_data('Day11Data.txt')))

def parttwo(rawdata):

  count = 0

  for pair in rawdata:

    (a,b) = (pair[0][0],pair[0][1])
    (c,d) = (pair[1][0],pair[1][1])

    if (a > c) or (a == c and d > b):
      a, b, c, d = c, d, a , b

    if b >= c:
      count +=1

  return count

print(parttwo(get_data('Day11Data.txt')))
    

       
       
        
       

       