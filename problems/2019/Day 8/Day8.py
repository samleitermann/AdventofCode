def get_data(file):
    with open(file, 'r') as f:
        data = list(map(int, f.read()))
    return data

data = get_data("/Users/sleitermann-long/Documents/AdventofCode/AdventofCode2019/Day 8/input.txt")

def split_layersandcount(data, H, W, layers =[], count = [],ans_1 = 0):
  i = 0

  #Splits data into individual layers and counts how many 0's in each layter
  while i < len(data):
    layer = data[i:i+H*W]
    counts = layer.count(0)

    count.append(counts)
    layers.append(layer)

    i += H*W

  return [layers, count]

def ans_1(layer, count):
    #Finds the layer with the minimum number of 0's
  minindex = count.index(min(count))
  #Finds the numbers of 1's and 2's and returns their multiplication
  count1 = layer[minindex].count(1)
  count2 = layer[minindex].count(2)

  return count1*count2

#Answer 1
dataset = split_layersandcount(data,25,6)
answer = ans_1(dataset[0],dataset[1])
print('Part 1: ', answer)

def ans_2(layer, image = []):
    #Sets up the initial layer
    image = layer[0]

    #Runs a loop for each entry in image that goes through the layers and finds the first value that is not a 2. Then adds replaces the entry in image with that value.
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
    #Split into rows, then take out brackets, 0's, and commas for readability. Then prints.
  tempanswer = str(answer2[i:i+25]).strip('[]').replace(',','')
  tempanswer = tempanswer.replace('0', " ")
  print(tempanswer)
  i += 25
