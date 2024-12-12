import argparse
from collections import deque

class Solution:
  filename_real_input = 'real_input.txt'
  filename_test_input = 'test_input.txt'

  def __init__(self, test=False):
    self.filename = self.filename_test_input if test else self.filename_real_input
    self.file = open(self.filename,'r').read()
    self.lines = self.file.splitlines()
    self.grid =self.create_grid()
    self.islands = self.getallislands()
    self.result = 0
    self.visited = set()

  def create_grid(self):
    #initialize a dictionary, and then traverse the lines adding the value at each grid point.
    grid = {}
    for i, row in enumerate(self.lines):
      for j, val in enumerate(row):
        grid[(i,j)] = val
    return grid

  def island(self, start):
    visited = set()
    Q = deque([start])

    while Q:
      current = Q.popleft()
      if current in visited:
        continue
      else:
        visited.add(current)

      i, j = current
      neighbors = [(i, j + 1), (i, j - 1), (i + 1, j), (i - 1, j)]

      for neigh in neighbors:
        if neigh in self.grid and self.grid[neigh] == self.grid[current]:
          Q.append(neigh)

    return visited

  def calc_perimeter(self,isle):
    perimeter = 0
    for patch in isle:
      i, j = patch
      neighbors = [(i, j + 1), (i, j - 1), (i + 1, j), (i - 1, j)]
      for neigh in neighbors:
        if neigh not in self.grid or self.grid[neigh] != self.grid[patch]:
          perimeter += 1
    return perimeter

  def getallislands(self):

    islands = []
    checked = set()

    for point in self.grid:
      if point not in checked:
        isle = self.island(point)
        for pt in isle:
          checked.add(pt)
        islands.append(isle)
    return islands



  def part1(self):
    price = 0
    islands = self.getallislands()

    for isle in islands:
      area = len(isle)
      peri = self.calc_perimeter(isle)
      price += area * peri

    return price

  def part2(self):
    pass
  
if __name__ == '__main__':
  parser = argparse.ArgumentParser('Solution file')
  parser.add_argument('-part', required=True, type=int, help='Part (1/2)')
  parser.add_argument('-test', required=True, type=str, help='Test mode (True/False)')
  args = parser.parse_args()
  test = True if args.test in ['True','true'] else False
  solution = Solution(test=test)
  result = solution.part1() if args.part == 1 else solution.part2()
  print(f'Result for Part=={args.part} & Test=={test} : {result}')
