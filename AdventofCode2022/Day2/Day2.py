def get_data(file):
  data=[]
  round = []
  with open(file, 'r') as f:
     for line in f:
       round.append(line[0])
       round.append(line[2])
       data.append(round)
       round = []
  return data

def get_data2(file):
  data=[]
  with open(file, 'r') as f:
     for line in f:
       data.append(line.rstrip())
  return data

def partone(rawdata):
  beats = {'A':'Z', 'B':'X', 'C':'Y', 'X':'C', 'Y':'A', 'Z':'B'}
  score = {'X':1, 'Y':2, 'Z':3}

  total = 0
  for round in rawdata:
    total += score[round[1]]

    if round[0] == beats[round[1]]:
      total += 6
    elif round[1]==beats[round[0]]:
      total += 0
    else:
      total += 3

  return total

print(partone(get_data('Day11Data.txt')))

def parttwo(rawdata):

  score = {'A X':3, 'A Y':4, 'A Z':8,
	 'B X':1, 'B Y':5, 'B Z':9,
	 'C X':2, 'C Y':6, 'C Z':7}

  total = 0

  for round in rawdata:
    #print(round)
    #print(score[round])
    total += score[round]

  return total

print(parttwo(get_data2('Day11Data.txt')))