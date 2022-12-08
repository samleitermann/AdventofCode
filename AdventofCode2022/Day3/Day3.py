def partone(file):
  
  data=[]

  priority =  {'a':1,'b':2,'c':3,'d':4,'e':5,'f':6,'g':7,'h':8,'i':9,'j':10,'k':11,'l':12,'m':13,'n':14,'o':15,'p':16,'q':17,'r':18,'s':19,'t':20,'u':21,'v':22,'w':23,'x':24,'y':25,'z':26,'A':27,'B':28,'C':29,'D':30,'E':31,'F':32,'G':33,'H':34,'I':35,'J':36,'K':37,'L':38,'M':39,'N':40,'O':41,'P':42,'Q':43,'R':44,'S':45,'T':46,'U':47,'V':48,'W':49,'X':50,'Y':51,'Z':52}
  
  
  with open(file, 'r') as f:
    
    total = 0
    for line in f:

      compartment1 = []
      compartment2= []
      
      size = len(line.rstrip())
      
      for i in range(int(size/2)):
        compartment1.append(line[i])
      for i in range(int(size/2)):
        index = i+int(size/2)
        compartment2.append(line[index])

      compare = list(set(compartment1).intersection(compartment2))
      
      total += priority[compare[0]]

      data.append(compare)
      compare = []  
  return total
  
print(partone('Day11Data.txt'))


def parttwo(file):
  
  priority =  {'a':1,'b':2,'c':3,'d':4,'e':5,'f':6,'g':7,'h':8,'i':9,'j':10,'k':11,'l':12,'m':13,'n':14,'o':15,'p':16,'q':17,'r':18,'s':19,'t':20,'u':21,'v':22,'w':23,'x':24,'y':25,'z':26,'A':27,'B':28,'C':29,'D':30,'E':31,'F':32,'G':33,'H':34,'I':35,'J':36,'K':37,'L':38,'M':39,'N':40,'O':41,'P':42,'Q':43,'R':44,'S':45,'T':46,'U':47,'V':48,'W':49,'X':50,'Y':51,'Z':52}
  
  
  with open(file, 'r') as f:

    elves = []
    common = []
    total = 0
    
    total = 0
    for line in f:
      elf = []
      for i in range(len(line)-1):
        elf.append(line[i])
      elves.append(elf)

    groups = 0

    while groups < len(elves):
      compare1 = set(elves[groups]).intersection(elves[groups+1])
      compare2 = list(compare1.intersection(elves[groups+2]))

      common.append(compare2[0])

      groups +=3

    for comm in common:
      total += priority[comm]
      
      
  return total
  
print(parttwo('Day11Data.txt'))

