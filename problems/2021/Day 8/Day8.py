def get_data(file):
  with open(file, encoding='utf-8') as f:
    data = f.read()
    #split by lines
    inputs = data.split('\n')
    parsed = []
    #Split by the delimiter
    for line in inputs:
      x,y = line.split('|')
      parsed.append([x,y])
        
  return parsed

data = get_data('Day5Data.txt')

def part_one(data):
  count = 0
  for dat in data:
    #Split into individual digits
    digits = dat[1].split()
    for dig in digits:
      #check to see if they were one of the known options and count
      if len(dig) in (2,3,4,7):
        count +=1 
  
  return count

def part_two(data):
  s = 0
  for dat in data:
    #Find the lengths of each of the signal patterns
    l = {len(s): set(s) for s in dat[0].split()}
    #create an empty string to add digits to
    n = ''
    #loop over the digits in the output
    for o in map(set, dat[1].split()):
      #mask with the known digits to determine pattern. When case is matched, add digit to the string. Matching length, digits in common with known options.
      match len(o), len(o&l[4]), len(o&l[2]):
        case 2,_,_: n += '1'
        case 3,_,_: n += '7'
        case 4,_,_: n += '4'
        case 7,_,_: n += '8'
        case 5,2,_: n += '2'
        case 5,3,1: n += '5'
        case 5,3,2: n += '3'
        case 6,4,_: n += '9'
        case 6,3,1: n += '6'
        case 6,3,2: n += '0'
    #convert to int and add to total
    s += int(n)

  return s






