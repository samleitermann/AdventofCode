import argparse
import re

class Solution:
  filename_real_input = 'real_input.txt'
  filename_test_input = 'test_input.txt'
  
  def __init__(self, test=False):
    self.filename = self.filename_test_input if test else self.filename_real_input
    self.file = open(self.filename,'r').read()
    self.lines = self.file.splitlines()

  def parse_instructions(self):
    A = re.findall(r'(\d+)',self.lines[0])
    B = re.findall(r'(\d+)',self.lines[1])
    C = re.findall(r'(\d+)',self.lines[2])
    instructions = [int(i) for i in re.findall(r'(\d+)',self.lines[4])]

    return int(A[0]), int(B[0]), int(C[0]), instructions

  def combo_instr(self, x, A, B, C):
    if x in [0,1,2,3]:
      return x
    elif x == 4:
      return A
    elif x == 5:
      return B
    elif x == 6:
      return C
    return -1

  def run(self, A, B, C):
    inst_pointer = 0
    data = self.parse_instructions()
    instructions = data[3]

    output = []

    while True:
      if inst_pointer >= len(instructions):
        return output
      command = instructions[inst_pointer]
      op = instructions[inst_pointer+1]
      combo = self.combo_instr(op, A, B, C)

      if command == 0:
        A = A// 2**combo
        inst_pointer += 2
      elif command ==1:
        B = B^op
        inst_pointer += 2
      elif command == 2:
        B = combo % 8
        inst_pointer += 2
      elif command == 3:
        if A != 0:
          inst_pointer = op
        else:
          inst_pointer += 2
      elif command == 4:
        B = B ^ C
        inst_pointer += 2
      elif command == 5:
        output.append(int(combo % 8))
        inst_pointer += 2
      elif command == 6:
        B = A // (2 ** combo)
        inst_pointer += 2
      elif command == 7:
        C = A // (2 ** combo)
        inst_pointer += 2



  def part1(self):
    data = self.parse_instructions()
    return self.run(data[0],data[1],data[2])

  
  def part2(self):
    data = self.parse_instructions()
    instructions = data[3]
    possibles = {0:[x for x in range(8)]}
    A = data[0]
    B = data[1]
    C = data[2]

    for exponent in range(1, len(instructions)):
      possibles[exponent] = []
      for p in possibles[exponent-1]:
        for q in range(8):
          if p ==0:
            continue
          regA = 8*p+q
          out = self.run(regA, B, C)
          l = len(out)
          if out == instructions[len(instructions)-l:]:
            possibles[exponent].append(regA)
          if out == instructions:
            return regA
  
if __name__ == '__main__':
  parser = argparse.ArgumentParser('Solution file')
  parser.add_argument('-part', required=True, type=int, help='Part (1/2)')
  parser.add_argument('-test', required=True, type=str, help='Test mode (True/False)')
  args = parser.parse_args()
  test = True if args.test in ['True','true'] else False
  solution = Solution(test=test)
  result = solution.part1() if args.part == 1 else solution.part2()
  print(f'Result for Part=={args.part} & Test=={test} : {result}')
