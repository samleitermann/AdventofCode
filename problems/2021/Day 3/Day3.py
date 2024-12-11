from collections import Counter

def get_data(file):
    with open(file, encoding='utf-8') as f:
        data = f.read()
        inputs = data.splitlines()
    return inputs

diagnostic = get_data('Day3Data.txt')

def part_one(diaglist):
  gamma = ''
  epsilon = ''

  for i in range(len(diaglist[0])):
    common = Counter([x[i] for x in diaglist])
    
    if common['0'] > common['1']:
      gamma += '0'
      epsilon += '1'
    else:
      gamma += '1'
      epsilon += '0'

  return (int(gamma,2)*int(epsilon,2))

print(part_one(diagnostic))

def part_two_oxygen(diaglist):
  oxrating = ''

  for i in range(len(diaglist[0])):
    common = Counter([x[i] for x in diaglist])

    if common['0'] > common['1']:
      diaglist = [x for x in diaglist if x[i] == '0']
    else:
      diaglist = [x for x in diaglist if x[i] == '1']

    oxrating = diaglist[0]
  return int(oxrating,2)

def part_two_C02(diaglist):
  C02rating = ''

  for i in range(len(diaglist[0])):
    common = Counter([x[i] for x in diaglist])

    if common['0'] > common['1']:
      diaglist = [x for x in diaglist if x[i] == '1']
    else:
      diaglist = [x for x in diaglist if x[i] == '0']
      
    if diaglist:
      C02rating = diaglist[0]
    
  return int(C02rating,2)

print(part_two_C02(diagnostic)*part_two_oxygen(diagnostic))


