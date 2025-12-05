import argparse
import re

import time

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

  def parse_file(self):

    raw_ranges = []
    ingredients = []

    ranges = []
    #Add all the ingredient ID ranges to an array, then when you hit the space between ranges and IDs
    #switch arrays and add all the ingredient IDs to an array.
    flag = False
    for line in self.lines:
        if line == '':
          flag = True
          continue
        if not flag:
            raw_ranges.append(line)
        if flag:
            ingredients.append(line)

    #Turn ID ranges into tuples representing intervals.
    for ran in raw_ranges:

        start, end = ran.split('-')
        ranges.append((int(start), int(end)))

    return ranges, ingredients

  def merge_intervals(self):
    #Basic interval merge, sort the intervals by start value and then compare ending and starting,
    #merging as appropriate.
      intervals = self.parse_file()[0]

      intervals.sort(key=lambda x:x[0])

      merged_intervals = [intervals[0]]

      for current_start, current_end in intervals[1:]:

          last_start, last_end = merged_intervals[-1]

          if current_start <= last_end:
              new_end = max(last_end, current_end)
              merged_intervals[-1] = (last_start, new_end)
          else:
              merged_intervals.append((current_start,current_end))

      return merged_intervals



  def part1(self):
    start = time.perf_counter()
    ingredient_ranges = self.merge_intervals()
    ingredients = self.parse_file()[1]

    fresh = []
    #for each ingredient, check if it is in one of the intervals. Exit early if it is.
    for ingredient in ingredients:
        for ranges_start, ranges_end in ingredient_ranges:
            if ranges_start <= int(ingredient) <= ranges_end:
                fresh.append(ingredient)
                continue
    end = time.perf_counter()

    print(end-start)
    return len(fresh)
  
  def part2(self):
      start = time.perf_counter()
      ingredient_ranges = self.merge_intervals()

      freshness = 0
    #because we've combined intervals, we just need to find the length of each interval and add them up.
      for ranges_start, ranges_end in ingredient_ranges:
          freshness += ranges_end - ranges_start +1

      end = time.perf_counter()

      print(end-start)
      return freshness

  
if __name__ == '__main__':
  parser = argparse.ArgumentParser('Solution file')
  parser.add_argument('-part', required=True, type=int, help='Part (1/2)')
  parser.add_argument('-test', required=True, type=str, help='Test mode (True/False)')
  args = parser.parse_args()
  test = True if args.test in ['True','true'] else False
  solution = Solution(test=test)
  result = solution.part1() if args.part == 1 else solution.part2()
