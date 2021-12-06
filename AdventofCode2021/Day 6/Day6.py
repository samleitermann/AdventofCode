def get_data(file):
    with open(file, encoding='utf-8') as f:
        data = f.read()
        inputs = data.split(',')
        intinputs = list(map(int,inputs))
    return intinputs



data = get_data('Day6Data.txt')

def fish_pop(data,days):
  school = {0:0,1:0,2:0,3:0,4:0,5:0,6:0,7:0,8:0}

  total = len(data)

  for fish in data:
      school[fish] += 1

  for day in range(days):

      placeholder = school[0]
      school[0] = school[1]
      school[1] = school[2]
      school[2] = school[3]
      school[3] = school[4]
      school[4] = school[5]
      school[5] = school[6]
      school[6] = school[7]
      school[7] = school[8]
      school[6] += placeholder
      school[8] = placeholder

      total += placeholder

  return total

print(fish_pop(data,256))