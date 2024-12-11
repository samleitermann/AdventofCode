from numpy import median, mean, floor, ceil

def get_data(file):
    with open(file, encoding='utf-8') as f:
        data = f.read()
        inputs = data.split(',')
        intinputs = list(map(int,inputs))
    return intinputs



data = get_data('Day7Data.txt')

def fuelconsumption_1(x):
  return sum(abs(x - median(x)))

print(fuelconsumption_1(data))

def fuelconsumption_2(x):
  fuel = lambda d: d*(d+1)/2
  
  return (min(sum(fuel(abs(x - floor(mean(x))))),
          sum(fuel(abs(x - ceil(mean(x)))))))

print('answer 1:',int(fuelconsumption_1(data)), ' answer 2:',int(fuelconsumption_2(data)))