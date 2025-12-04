import argparse
import re

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

    total = 0

    for bank in self.lines:

        start = 0
        end = len(bank) - 1
        digits = []


        while start +1 < end <= len(bank):
            search_area = bank[start:end]
            digit = max(search_area)
            digits.append(digit)

            start += search_area.index(digit) + 1
            end += 1

        total += int("".join(digits)+ bank[end - 1 :])


    return total

  
  def part2(self):

      total_2 = 0

      for bank in self.lines:

          start = 0
          end = len(bank) - 11
          digits_2 = []

          while start + 1 < end <= len(bank):
              search_area = bank[start:end]
              digit = max(search_area)
              digits_2.append(digit)

              start += search_area.index(digit) + 1
              end += 1

          total_2 += int("".join(digits_2) + bank[end - 1:])

      return total_2
  
if __name__ == '__main__':
  parser = argparse.ArgumentParser('Solution file')
  parser.add_argument('-part', required=True, type=int, help='Part (1/2)')
  parser.add_argument('-test', required=True, type=str, help='Test mode (True/False)')
  args = parser.parse_args()
  test = True if args.test in ['True','true'] else False
  solution = Solution(test=test)
  result = solution.part1() if args.part == 1 else solution.part2()
  print(result)