
data = open('Day5Data.txt', 'r')

def structure(file):

  levels, instructions = [section.split('\n') for section in file.read().split("\n\n")]
  
  levels = [crate.replace("    "," [X] ") for crate in levels[:-1]]
  levels = [[crate[1] for crate in level.split()] for level in levels]
  stacks = [[] for _ in range(len(levels[0]))]

  for level in reversed(levels):
    for index, crate in enumerate(level):
      if crate != 'X':
        stacks[index].append(crate)

  return(instructions,levels, stacks)

def PartOne(file):

  instructions, levels, stacks = structure(file)

  for instruction in instructions:

    quantity, from_stack_order, to_stack_order = [int(i) for i in instruction.split(" ") if i.isnumeric()]

    while quantity != 0:

      stacks[to_stack_order-1].append(stacks[from_stack_order-1].pop())
      quantity -=1

  print("Part 1 ", end = "")
  [print(stack[-1], end='') for stack in stacks]
  print()

#PartOne(data)

def PartTwo(file):

  instructions, levels, stacks = structure(file)

  for instruction in instructions:

    quantity, from_stack_order, to_stack_order = [int(i) for i in instruction.split(" ") if i.isnumeric()]
    from_stack = stacks[from_stack_order-1]
    stacks[to_stack_order-1].extend(from_stack[len(from_stack)-quantity:])
    stacks[from_stack_order-1] = from_stack[:len(from_stack)-quantity]

  print("Part 2 ", end = "")
  [print(stack[-1], end='') for stack in stacks]
  print()



PartTwo(data)


