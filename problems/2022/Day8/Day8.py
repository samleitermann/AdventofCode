def get_data(file):

  with open(file, 'r') as f:
     data = f.read().splitlines()
  return data

def partone(file):

  horizontal_length = len(file[0])
  vertical_length = len(file)

  visible_trees = horizontal_length*2+(vertical_length-2)*2

  for row_index, row in enumerate(file):
    if row_index == 0 or row_index == vertical_length-1:
      continue
    for tree_index, tree_height in enumerate(row):
      if tree_index == 0 or tree_index == horizontal_length-1:
        continue

      tree_height = int(tree_height)
      visible_from_left = all(int(height) < tree_height for height in row[:tree_index])
      visible_from_right = all(int(height)< tree_height for height in row[tree_index+1:])
      top_trees = [row[tree_index] for row in file[:row_index]]
      bottom_trees = [row[tree_index] for row in file[row_index+1:]]
      visible_from_top = all(int(height) < tree_height for height in top_trees)
      visible_from_bottom = all(int(height) < tree_height for height in bottom_trees)

      visible_trees += any([visible_from_left, visible_from_right, visible_from_top, visible_from_bottom])


  print(horizontal_length, vertical_length,visible_trees)

partone(get_data('Day8Data.txt'))

def get_vision(tree_height, tree_list):
  vision = 0
  index = 0
  while index != len(tree_list):
    vision +=1
    if int(tree_list[index]) >= tree_height:
      return vision
    index += 1

  return vision


def parttwo(file):
  highest_scenic_score = 0

  horizontal_length = len(file[0])
  vertical_length = len(file)

  for row_index, row in enumerate(file):
    if row_index == 0 or row_index == vertical_length-1:
      continue
    for tree_index, tree_height in enumerate(row):
      if tree_index == 0 or tree_index == horizontal_length-1:
        continue

      tree_height = int(tree_height)
      left_vision = get_vision(tree_height, row[:tree_index][::-1])
      right_vision = get_vision(tree_height, row[tree_index+1:])
      top_trees = [row[tree_index] for row in file[:row_index]]
      bottom_trees = [row[tree_index] for row in file[row_index+1:]]
      top_vision = get_vision(tree_height, top_trees[::-1])
      bottom_vision = get_vision(tree_height, bottom_trees)

      print(left_vision, right_vision, top_vision, bottom_vision)

      vision_score = left_vision*right_vision*top_vision*bottom_vision
      print(vision_score)

      if vision_score > highest_scenic_score:
        highest_scenic_score = vision_score

  print(highest_scenic_score)


parttwo(get_data('Day8Test.txt'))
