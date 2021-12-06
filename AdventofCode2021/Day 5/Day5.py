from collections import Counter

def get_data(file):
    with open(file, encoding='utf-8') as f:
        data = f.read()
        inputs = data.splitlines()
    return inputs

lines = get_data('Day5Data.txt')

points = []

for l in lines:
  point1 = l.split('->')[0]
  point2 = l.split('->')[1]

  x_1 = int(point1.split(',')[0])
  y_1 = int(point1.split(',')[1])

  x_2 = int(point2.split(',')[0])
  y_2 = int(point2.split(',')[1])
  
  if x_1 == x_2 or y_1 == y_2:
    for x in range(min(x_1,x_2), max(x_1,x_2)+1):
      for y in range(min(y_1,y_2), max(y_1,y_2)+1):
        points.append((x,y))

print(len([x for (x,y) in Counter(points).items() if y>1]))

points = []
for l in lines:

  point1 = l.split('->')[0]
  point2 = l.split('->')[1]

  x_1 = int(point1.split(',')[0])
  y_1 = int(point1.split(',')[1])

  x_2 = int(point2.split(',')[0])
  y_2 = int(point2.split(',')[1])
  
	
  dx = 1 if x_2>x_1 else -1
  dy = 1 if y_2>y_1 else -1

  if x_1 == x_2:
    dx = 0
  if y_1 == y_2:
    dy = 0

  points.append((x_1,y_1))
	
  while x_1 != x_2 or y_1 != y_2:
    x_1 += dx
    y_1 += dy
    points.append((x_1,y_1))

print(len([x for (x,y) in Counter(points).items() if y>1]))
  









