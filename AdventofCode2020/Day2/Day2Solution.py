def get_data(file):
    with open(file, 'r') as f:
        data = [line.strip() for line in f]
    return data

passwords = get_data("Day2Input.txt")

#Set initial counterse
part_one = 0
part_two = 0

#split into necessary data
for group in passwords:
  count, letter, password = group.split()
  letter = letter[:1]
  low,high = count.split("-")

#turn into integers
  low = int(low)
  high = int(high)

#count occurences
  count = password.count(letter)

#check if meets criteria
  if count >= low and count <= high:
      part_one += 1

  #adjust for indexing
  low -=1
  high -=1

  #check
  if (password[low] == letter) != (password[high] == letter):
    part_two += 1
  else:
      pass

print ("Part 1: ",part_one)
print ("Part 2: ", part_two)
