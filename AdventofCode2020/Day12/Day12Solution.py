import math

def get_data(file):
    with open(file, 'r') as f:
        data = list(f.read().split("\n"))
    return data

data = get_data('Day12Input.txt')

def split_directions(data):
  directions = []


  for i in range(len(data)):
    directions.append([data[i][:1],int(data[i][1:])])
  
  return directions

def part_one(directions):
  ship_xy = [0,0]
  ship_angle = 0

  for i in range(len(directions)):

    if directions[i][0] == 'N':
      ship_xy[1] += directions[i][1]
    
    elif directions[i][0] == 'S':
      ship_xy[1] -= directions[i][1]
    
    elif directions[i][0] == 'E':
      ship_xy[0] += directions[i][1]
    
    elif directions[i][0] == 'W':
      ship_xy[0] -= directions[i][1]
    
    elif directions[i][0] == 'L':
      ship_angle += math.radians(directions[i][1])
    
    elif directions[i][0] == 'R':
      ship_angle -= math.radians(directions[i][1])
    
    elif directions[i][0] == 'F':
      ship_xy[0] += directions[i][1]*math.cos(ship_angle)
      ship_xy[1] += directions[i][1]*math.sin(ship_angle)
    
  return abs(ship_xy[0]) + abs(ship_xy[1])


print('Part One:', part_one(split_directions(data)))



def part_two(directions):

  waypoint = [10,1]
  ship_xy = [0,0]
  ship_angle = 0
  

  for i in range(len(directions)):

    if directions[i][0] == 'N':

      waypoint[1] += directions[i][1]
    
    elif directions[i][0] == 'S':
      waypoint[1] -= directions[i][1]
    
    elif directions[i][0] == 'E':
      waypoint[0] += directions[i][1]
    
    elif directions[i][0] == 'W':
      waypoint[0] -= directions[i][1]
    
    elif directions[i][0] == 'L':
      angle = directions[i][1]
      angle = (angle/90) % 4

      waypoint_diff = [(waypoint[0]-ship_xy[0]),(waypoint[1]-ship_xy[1])]

      if angle == 1:
          waypoint_diff = [-1*waypoint_diff[1],waypoint_diff[0]]
      elif angle == 2:
          waypoint_diff = [-1*waypoint_diff[0], -1*waypoint_diff[1]]
      elif angle == 3:
          waypoint_diff = [waypoint_diff[1],-1*waypoint_diff[0]]
      
      waypoint[0] = waypoint_diff[0] + ship_xy[0]
      waypoint[1] = waypoint_diff[1] + ship_xy[1]
    
    elif directions[i][0] == 'R':
      angle = directions[i][1]
      angle = (angle/90) % 4

      waypoint_diff = [(waypoint[0]-ship_xy[0]),(waypoint[1]-ship_xy[1])]

      if angle == 1:
          waypoint_diff = [waypoint_diff[1], -1*waypoint_diff[0]]
      elif angle == 2:
          waypoint_diff = [-1*waypoint_diff[0], -1*waypoint_diff[1]]
      elif angle == 3:
          waypoint_diff = [-1*waypoint_diff[1],waypoint_diff[0]]
      
      waypoint[0] = waypoint_diff[0] + ship_xy[0]
      waypoint[1] = waypoint_diff[1] + ship_xy[1]

    elif directions[i][0] == 'F':
      waypoint_diff = [(waypoint[0]-ship_xy[0]),(waypoint[1]-ship_xy[1])]

      ship_xy[0] += (waypoint[0]-ship_xy[0])*directions[i][1]
      ship_xy[1] += (waypoint[1]-ship_xy[1])*directions[i][1]
      waypoint[0] = waypoint_diff[0] + ship_xy[0]
      waypoint[1] = waypoint_diff[1] + ship_xy[1]
  

  return abs(ship_xy[0]) + abs(ship_xy[1])

print('Part Two:', part_two(split_directions(data)))

    
