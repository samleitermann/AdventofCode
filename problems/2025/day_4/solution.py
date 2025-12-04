import argparse
import re
from aoctools import *

aocd = AOCD(2025, 4)

lists = aocd.slist

grid = []
padding = [0]*137

grid.append(padding)

for row in lists:
    new_row = "."+row+"."
    temp_row = []

    for char in new_row:
        if char == ".":
            temp_row.append(0)
        else:
            temp_row.append(1)

    grid.append(temp_row)

grid.append(padding)


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
      reachable = 0

      reachable_list = []

      for i in range(1, len(grid[0]) - 1):
          for j in range(1, len(grid) - 1):
              if grid[i][j] == 1:
                  count = grid[i - 1][j - 1] + grid[i - 1][j] + grid[i - 1][j + 1] + grid[i][j - 1] + grid[i][j + 1] + \
                          grid[i + 1][j - 1] + grid[i + 1][j] + grid[i + 1][j + 1]
                  reachable_list.append((i, j))

                  if count < 4:
                      reachable += 1
      return reachable
  
  def part2(self):
      total_reachable = 0

      while reachable > 0:
          reachable = 0
          reachable_list = []
          for i in range(1, len(grid[0]) - 1):
              for j in range(1, len(grid) - 1):
                  if grid[i][j] == 1:
                      count = grid[i - 1][j - 1] + grid[i - 1][j] + grid[i - 1][j + 1] + grid[i][j - 1] + grid[i][
                          j + 1] + \
                              grid[i + 1][j - 1] + grid[i + 1][j] + grid[i + 1][j + 1]

                      if count < 4:
                          reachable += 1
                          grid[i][j] = 0

          total_reachable += reachable

      return total_reachable
  
if __name__ == '__main__':
  parser = argparse.ArgumentParser('Solution file')
  parser.add_argument('-part', required=True, type=int, help='Part (1/2)')
  parser.add_argument('-test', required=True, type=str, help='Test mode (True/False)')
  args = parser.parse_args()
  test = True if args.test in ['True','true'] else False
  solution = Solution(test=test)
  result = solution.part1() if args.part == 1 else solution.part2()
