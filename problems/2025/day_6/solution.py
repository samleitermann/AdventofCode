import argparse
import re
import numpy as np
from rich import columns


class Solution:
  filename_real_input = 'real_input.txt'
  filename_test_input = 'test_input.txt'
  
  @staticmethod
  def get_nums(string: str) -> list[int]:
    return list(map(int, re.findall(r'[-+]?\d+', string)))
  
  def __init__(self, test=False):
    self.filename = self.filename_test_input if test else self.filename_real_input
    self.file = open(self.filename,'r').read()
    self.lines = self.file.splitlines()
    
  def part1(self):

    #-------Data Parsing------#
    #Initialize a lines array, split each line into its component integers
    lines = []

    rows  = len(self.lines)

    for line in self.lines[0:rows-1]:
        lines.append([int(x) for x in line.split()])

    lines.append([x for x in self.lines[rows-1].split()])

    columns = len(lines[0])

    problems = [[] for _ in range(columns)]

    for line in lines:
        for i in range(0,len(line)):
            problems[i].append(line[i])

    #-----Calculations-----#

    total = 0
    for prob in problems:
        if prob[rows-1] == "*":
            total += np.prod(prob[0:rows-1])
        if prob[rows-1] == "+":
            total += np.sum(prob[0:rows-1])

    return total
  
  def part2(self):
    #-----Define Objects and Transpose Columns to Rows
    numbers = self.lines[:-1]
    operators = self.lines[-1]
    transposed_nums = list(zip(*numbers))

    #-----Use number of Operators to check how many problems-----#
    problem_num = len(operators.split())
    problems = [[] for _ in range(problem_num)]

    #-----Create problem arrays, splitting at lines of all whitespace-----#
    i = 0
    for num in transposed_nums:
        if  not all([char == ' ' for char in num]):
            problems[i].append(num)
        else:
            i += 1

    #-----Join number strings into integers, then use operator to calculate total-----#
    j = 0
    total = 0
    for prob in problems:
        new_prob = ["".join(num) for num in prob]
        new_prob = [int(num) for num in new_prob]
        if operators.split()[j] == "*":
            total += np.prod(new_prob)
        if operators.split()[j] == "+":
            total += np.sum(new_prob)
        j += 1

    return total
  
if __name__ == '__main__':
  parser = argparse.ArgumentParser('Solution file')
  parser.add_argument('-part', required=True, type=int, help='Part (1/2)')
  parser.add_argument('-test', required=True, type=str, help='Test mode (True/False)')
  args = parser.parse_args()
  test = True if args.test in ['True','true'] else False
  solution = Solution(test=test)
  result = solution.part1() if args.part == 1 else solution.part2()
