origprogram = open('Day2Input.txt').read().split(",")

noun = 0
verb = 0

for j in range(0,99):
  for i in range(0,99):
    count = 0
    program = [
    1, 0, 0, 3, 1, 1, 2, 3, 1, 3, 4, 3, 1, 5, 0, 3, 2, 10, 1, 19, 2, 9, 19, 23,
    2, 13, 23, 27, 1, 6, 27, 31, 2, 6, 31, 35, 2, 13, 35, 39, 1, 39, 10, 43, 2,
    43, 13, 47, 1, 9, 47, 51, 1, 51, 13, 55, 1, 55, 13, 59, 2, 59, 13, 63, 1,
    63, 6, 67, 2, 6, 67, 71, 1, 5, 71, 75, 2, 6, 75, 79, 1, 5, 79, 83, 2, 83,
    6, 87, 1, 5, 87, 91, 1, 6, 91, 95, 2, 95, 6, 99, 1, 5, 99, 103, 1, 6, 103,
    107, 1, 107, 2, 111, 1, 111, 5, 0, 99, 2, 14, 0, 0
    ]
    noun = i
    verb = j
    program[1] = noun
    program[2] = verb
    length = len(program)/4
    while count < length:
        prog = program[4 * count:4 * count + 4]  #grab program sublist
        if prog[0] == 1:
            index1 = prog[1]
            index2 = prog[2]
            index3 = prog[3]
            newprog = program[index1] + program[index2]
            program[index3] = newprog
        elif prog[0] == 2:
            index1 = prog[1]
            index2 = prog[2]
            index3 = prog[3]
            newprog = program[index1]*program[index2]
            program[index3] = newprog
        elif prog[0] == 99:
            break
        count += 1
    if program[0] == 19690720:
      print(noun)
      print(verb)
      print("Voila!")
      exit()
    else:
      print(noun)
      print(verb)
