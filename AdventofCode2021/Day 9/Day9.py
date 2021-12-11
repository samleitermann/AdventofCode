def get_heights(file):
  #Process the data
  heights = [[int(c) for c in line.strip()] for line in open(file, "r").readlines()]
  return heights

data = get_heights("C:/Users/samle/OneDrive/Documents/GitHub/AdventofCode/AdventofCode2021/Day 9/Day9Data.txt")

rowlength = len(data[0]) #M
columnlength = len(data) #N

def get_neighbours(y,x):
  #Get the neighbors of a certain point.
  neigh = [(y+1,x), (y-1,x),(y,x+1), (y,x-1)]
  return [(a,b) for a,b in neigh if 0 <= a < columnlength and 0 <= b < rowlength]

def part_one(data, N, M):

  lowpoints = []
  #iterate over the rows and columns
  for y in range(N):
    for x in range(M):
      #check neighbors of a point and add if it is a lowpoint
      if all(data[y][x] < data[a][b] for a,b in get_neighbours(y,x)):
        lowpoints.append((y,x))
  
  return lowpoints, sum(data[y][x] + 1 for y, x in lowpoints)

print(part_one(data,columnlength,rowlength)[1])

# Part 2
def get_basin(data,y, x):
    #Initialize a basin with just the point itself.
    basin = {(y, x)}
    #Iterate over neighbors, searching for lowerpoints, and then add them to the set using an OR and recursion.
    for a, b in get_neighbours(y, x):
        if data[y][x] < data[a][b] < 9:
            basin |= get_basin(data,a, b)
    return basin



basin_sizes = sorted([len(get_basin(data,y, x)) for y, x in part_one(data,columnlength,rowlength)[0]])

print(basin_sizes[-1]*basin_sizes[-2]*basin_sizes[-3])
