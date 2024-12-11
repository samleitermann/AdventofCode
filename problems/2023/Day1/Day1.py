import re

def get_data(file):
  data=[]
  with open(file, 'r') as f:
     for line in f:
       data.append(line.rstrip())
  return dsata



rawdata=get_data("day_01.txt")
test_data = get_data("TestData1.txt")

def partone(data):
  
  data_part_one = []
  calibration_sum = 0

  #strip out all non-numeric characters in string
  for str in data:
    newstr = ''.join(i for i in str if i.isdigit())
    data_part_one.append(newstr)

  for num in data_part_one:
    last_digit = num[-1]
    first_digit = num[0]

    calibration_value = int(first_digit+last_digit)

    calibration_sum += calibration_value

  return(calibration_sum)

def parttwo(data):

  data_part_two = []

  number_map = {
    "one": "o1e",
    "two": "t2o",
    "three": "t3e",
    "four": "f4r",
    "five": "f5e",
    "six": "s6x",
    "seven": "s7n",
    "eight": "e8t",
    "nine": "n9e"}


  for str in data:

    for k,v in number_map.items():
      str = str.replace(k,v)

    data_part_two.append(str)

  
  answer = partone(data_part_two)


  return(answer)

print(parttwo(rawdata))




