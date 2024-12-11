def get_data(file):
  data=[]
  with open(file, 'r') as f:
     for line in f:
       data.append(line)
  return data

def partone(file):

  print(file)

  for line in file:

    i=0
    print(len(line))

    while i <= len(line)-4:
      print(set(line[i:i+4]))
      print(line[i:i+4])
      if len(set(line[i:i+4])) == len(line[i:i+4]):
        return(i+4)
      i+=1

print(partone(get_data('Day2Data.txt')))

def parttwo(file):


  print(file)

  for line in file:

    i=0
    print(len(line))

    while i <= len(line)-14:
      print(set(line[i:i+14]))
      print(line[i:i+14])
      if len(set(line[i:i+14])) == len(line[i:i+14]):
        return(i+14)
      i+=1

print(parttwo(get_data('Day2Data.txt')))

 