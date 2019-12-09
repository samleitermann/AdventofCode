count1 = 0
count2 = 0

minimum = 240298
maximum = 784956

for n in range(minimum, maximum):
  #convert to string
  ns = str(n)
  #check for duplicates
  repeats = [ns.count(d) for d in set(ns)]
  #check for requirements and iterate
  if ns == ''.join(sorted(ns)) and max(repeats)>=2:
    count1 += 1
    if 2 in repeats:
      count2 += 1

print(count1, " ", count2)
