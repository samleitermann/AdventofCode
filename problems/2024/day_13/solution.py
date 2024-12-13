import argparse
import re

class Solution:
  filename_real_input = 'real_input.txt'
  filename_test_input = 'test_input.txt'
  
  def __init__(self, test=False):
    self.filename = self.filename_test_input if test else self.filename_real_input
    self.file = open(self.filename,'r').read()
    self.lines = self.file.splitlines()
    self.machines = self.machine_parse()

  def machine_parse(self):
    machine = re.compile(r"Button A: X\+(\d+), Y\+(\d+)\nButton B: X\+(\d+), Y\+(\d+)\nPrize: X=(\d+), Y=(\d+)")
    sections = self.file.strip().split('\n\n')
    results = []

    for sec in sections:

      match = machine.match(sec)
      results.append((int(match.group(1)), int(match.group(2)),
                      int(match.group(3)), int(match.group(4)),
                      int(match.group(5)), int(match.group(6))))
      # note to self, this is (ax, ay, bx, by, px, py)
    return results

  def solve_claw(self, mac):
      determinant = mac[0]*mac[3]-mac[2]*mac[1]
      a_num = mac[3]*mac[4]-mac[2]*mac[5]
      b_num = mac[0]*mac[5]-mac[1]*mac[4]

      a = a_num/determinant
      b = b_num/determinant

      if a % 1 != 0:
        return False
      if b % 1 != 0:
        return False

      return(int(a), int(b))

  def fix_coords(self):
    new_coords = []
    for mac in self.machines:
      new_coords.append((mac[0], mac[1], mac[2], mac[3], mac[4]+10000000000000,mac[5]+10000000000000 ))

    return new_coords


  def part1(self):
    tokens = 0

    for mach in self.machines:
      solution_1 = self.solve_claw(mach)
      if solution_1 and solution_1[0] <=100 and solution_1[1] <= 100:
        tokens += 3*solution_1[0] + solution_1[1]

    return  tokens

  
  def part2(self):
    tokens = 0

    for mach in self.fix_coords():
      solution_2 = self.solve_claw(mach)
      if solution_2:
        tokens += 3 * solution_2[0] + solution_2[1]

    return tokens
  
if __name__ == '__main__':
  parser = argparse.ArgumentParser('Solution file')
  parser.add_argument('-part', required=True, type=int, help='Part (1/2)')
  parser.add_argument('-test', required=True, type=str, help='Test mode (True/False)')
  args = parser.parse_args()
  test = True if args.test in ['True','true'] else False
  solution = Solution(test=test)
  result = solution.part1() if args.part == 1 else solution.part2()
  print(f'Result for Part=={args.part} & Test=={test} : {result}')
