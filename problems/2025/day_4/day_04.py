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

reachable = 0

reachable_list = []

for i in range(1,len(grid[0]) - 1):
    for j in range(1,len(grid) - 1):
        if grid[i][j] == 1:
            count = grid[i-1][j-1]+grid[i-1][j]+grid[i-1][j+1]+grid[i][j-1]+grid[i][j+1]+grid[i+1][j-1]+grid[i+1][j]+grid[i+1][j+1]
            reachable_list.append((i,j))

            if count < 4:
                reachable += 1

print(reachable)

total_reachable  = 0

while reachable > 0:
    reachable = 0
    reachable_list = []
    for i in range(1, len(grid[0]) - 1):
        for j in range(1, len(grid) - 1):
            if grid[i][j] == 1:
                count = grid[i - 1][j - 1] + grid[i - 1][j] + grid[i - 1][j + 1] + grid[i][j - 1] + grid[i][j + 1] + \
                        grid[i + 1][j - 1] + grid[i + 1][j] + grid[i + 1][j + 1]

                if count < 4:
                    reachable += 1
                    grid[i][j] = 0

    total_reachable += reachable

print(total_reachable)








