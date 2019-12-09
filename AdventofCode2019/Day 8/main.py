def get_data(file):
    with open(file, 'r') as f:
        data = list(map(int, f.read()))
    return data

data = get_data("Day8Input.txt")

def split_layersandcount(data, H, W, layers =[], count = [],ans_1 = 0):
  i = 0

  while i < len(data):
    layer = data[i:i+H*W]
    counts = layer.count(0)

    count.append(counts)
    layers.append(layer)
    
    i += H*W
  
  return [layers, count]

def ans_1(layer, count):

  minindex = count.index(min(count))

  count1 = layer[minindex].count(1)
  count2 = layer[minindex].count(2)

  return count1*count2

#Answer 1

dataset = split_layersandcount(data,25,6)
answer = ans_1(dataset[0],dataset[1])
print('Part 1: ', answer)

def ans_2(layer, image = []):

    image = layer[0]

    for i in range(len(image)):
      l = 0
      while layer[l][i] == 2:
        l+= 1
      image[i] = layer[l][i]

    return image

#Answer 2
answer2 = ans_2(dataset[0])

#Print 
i = 0
while i<=150:
  tempanswer = str(answer2[i:i+25]).strip('[]').replace(',','')
  tempanswer = tempanswer.replace('0', " ")
  print(tempanswer)
  i += 25













