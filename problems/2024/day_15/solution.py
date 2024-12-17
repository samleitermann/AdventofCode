import argparse

class Solution:
  filename_real_input = 'real_input.txt'
  filename_test_input = 'test_input.txt'
  
  def __init__(self, test=False):
    self.filename = self.filename_test_input if test else self.filename_real_input
    self.file = open(self.filename,'r').read()
    self.parts = self.file.split('\n\n')
    self.grid = self.parts[0].splitlines()
    self.moves = self.parts[1].replace('\n', '')
    self.movedict = {'<': (0,-1), '^': (-1,0), 'v': (1,0), '>': (0,1)}
    self.walls2 = self.warehouse2()[1]


  def parse_input(self):
    #parses the input and then splits it into constituent parts.
    boxes = {(i,j) for i, line in enumerate(self.grid) for j, char in enumerate(line) if char == 'O'}
    walls = {(i,j) for i, line in enumerate(self.grid) for j, char in enumerate(line) if char == '#'}
    robot = [(i,j) for i, line in enumerate(self.grid) for j, char in enumerate(line) if char == '@']
    assert len(robot) == 1
    robot = robot[0]

    return boxes, walls, robot

  def warehouse2(self):
    warehouse = self.parts[0].replace('#','##').replace('O','[]').replace('.','..').replace('@','@.').splitlines()
    box_lefts = {(i, j) for i, line in enumerate(warehouse) for j, char in enumerate(line) if char == '['}
    walls2 = {(i, j) for i, line in enumerate(warehouse) for j, char in enumerate(line) if char == '#'}
    robot = [(i, j) for i, line in enumerate(warehouse) for j, char in enumerate(line) if char == '@']
    assert len(robot) == 1
    robot = robot[0]

    return box_lefts, walls2, robot

  def add(self, coord1, coord2):
    #just adds tuples. Easy Peasy.
    return tuple(i+j for i,j in zip(coord1, coord2))

  def intersect_check(self, coords,boxlefts):

    if coords in boxlefts:
      return coords
    elif self.add(coords,(0,-1)) in boxlefts:
      return self.add(coords,(0,-1))
    else:
      return tuple()

  def try_move(self,start, direction, boxlefts):

    target = self.add(start,direction)

    if target in self.walls2:
      return [False, set()]

    nextbox = self.intersect_check(target,boxlefts)

    if not nextbox:
      return [True,set()]
    else:
      if direction == (0, -1):
        next_move = self.try_move(nextbox, direction, boxlefts)
        return [next_move[0], next_move[1] | {nextbox}]
      elif direction == (0, 1):
        next_move = self.try_move(self.add(nextbox, (0, 1)), direction,boxlefts)
        return [next_move[0], next_move[1] | {nextbox}]
      else:
        next_move1 = self.try_move(nextbox, direction, boxlefts)
        next_move2 = self.try_move(self.add(nextbox, (0, 1)), direction, boxlefts)
        return [next_move1[0] and next_move2[0], next_move1[1] | next_move2[1] | {nextbox}]

  def part1(self):
    robot = self.parse_input()[2]
    walls = self.parse_input()[1]
    boxes = self.parse_input()[0]

    for move in self.moves:
      direction = self.movedict[move]
      target1 = self.add(robot,direction)

      if target1 not in walls and target1 not in boxes:
        # if you're moving into an empty space, just do it.
        robot = target1
      else:
        #look at the next space
        target2 = target1
        while target2 in boxes:
          #keep stepping down the box line.
          target2 = self.add(target2,direction)
        if target2 in walls:
          #if we hit a wall, we're fucked so don't move.
          continue
        else:
          #if we hit an empty space, teleport the box right next to the robot to the end.
          robot = target1
          boxes.remove(target1)
          boxes.add(target2)

    return sum(100*i+j for i,j in boxes)
  
  def part2(self):
    robot = self.warehouse2()[2]
    boxlefts = self.warehouse2()[0]

    for move in self.moves:
      direction = self.movedict[move]
      move_bool, move_boxes = self.try_move(robot, direction, boxlefts)
      if move_bool:
        boxlefts = {box for box in boxlefts if box not in move_boxes} | {self.add(box, direction) for box in move_boxes}
        robot = self.add(robot, direction)

    return sum(100*i+j for i,j in boxlefts)
  
if __name__ == '__main__':
  parser = argparse.ArgumentParser('Solution file')
  parser.add_argument('-part', required=True, type=int, help='Part (1/2)')
  parser.add_argument('-test', required=True, type=str, help='Test mode (True/False)')
  args = parser.parse_args()
  test = True if args.test in ['True','true'] else False
  solution = Solution(test=test)
  result = solution.part1() if args.part == 1 else solution.part2()
  print(f'Result for Part=={args.part} & Test=={test} : {result}')
