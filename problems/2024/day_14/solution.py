import argparse, re
from collections import namedtuple, defaultdict
from math import prod
import numpy as np
import cv2

class Solution:
  filename_real_input = 'real_input.txt'
  filename_test_input = 'test_input.txt'
  
  def __init__(self, test=False):
    self.filename = self.filename_test_input if test else self.filename_real_input
    self.file = open(self.filename,'r').read()
    self.lines = self.file.splitlines()
    self.robots = self.get_robots()

  def get_robots(self):
    exp = re.compile(r"p=(-?\d+),(-?\d+) v=(-?\d+),(-?\d+)")
    robots = []

    robot = namedtuple("robot", ("pos_x", "pox_y", "v_x", "v_y"))

    for bot in self.lines:
      match = exp.match(bot)

      pos_x, pos_y, v_x, v_y = map(int,match.groups())
      robots.append(robot(pos_x, pos_y, v_x, v_y))

    return robots

  def simulate_robots(self, seconds):
    robot_state =[]
    height = 103
    width = 101

    for bot in self.robots:
      current_x = (bot.pos_x + seconds*bot.v_x) % width
      current_y = (bot.pox_y + seconds*bot.v_y) % height
      robot_state.append((current_x, current_y))

    return robot_state

  def find_mean(self, vals):
    return sum(vals) / len(vals)

  def find_variance(self,vals):

    mean = self.find_mean(vals)
    return self.find_mean([(val - mean)**2 for val in vals])/len(vals)

  def print_tree(self, seconds):
    state = self.simulate_robots(seconds)
    grid = np.zeros((103,101))
    i = 0
    while i <= 101:
      j = 0
      while j < 101:
        if (i,j) in state:
          grid[i][j] = 255
        j +=1
      i += 1
    cv2.imwrite(f"{seconds:04}.png", grid,[cv2.IMWRITE_JPEG_QUALITY, 90])



  def part1(self):
    height = 103
    width = 101

    quad_count = defaultdict(int)

    for bot in self.simulate_robots(100):

      bool_x = bot[0] < width // 2
      bool_y = bot[1] < height // 2

      if bot[0] == width // 2 or bot[1] == height // 2:
        continue
      else:
        quad_count[(bool_x, bool_y)] += 1

    return prod(quad_count.values())



  def part2(self):
    found = False
    secs = 0

    while not found:
      cur_x = [pos[0] for pos in self.simulate_robots(secs)]
      cur_y = [pos[1] for pos in self.simulate_robots(secs)]

      var_x = self.find_variance(cur_x)
      var_y = self.find_variance(cur_y)
      #If you uncomment this line, it produces close to 8000 pngs (I used this to create an animation.)
      #self.print_tree(secs)
      if var_x < 1 and var_y < 1:
        #self.print_tree(secs)
        return secs

      secs += 1

  
if __name__ == '__main__':
  parser = argparse.ArgumentParser('Solution file')
  parser.add_argument('-part', required=True, type=int, help='Part (1/2)')
  parser.add_argument('-test', required=True, type=str, help='Test mode (True/False)')
  args = parser.parse_args()
  test = True if args.test in ['True','true'] else False
  solution = Solution(test=test)
  result = solution.part1() if args.part == 1 else solution.part2()
  print(f'Result for Part=={args.part} & Test=={test} : {result}')
