from collections import deque

def get_data(file):
    #open the file and strip out trailing whitespace

    with open(file, 'r') as f:
        inp = f.read()

    return inp

def create_grid(inp):
    # initialize a dictionary, and then traverse the lines adding the value at each grid point.
    grid = {}
    for i, row in enumerate(inp.splitlines()):
        for j, val in enumerate(row):
            grid[(i, j)] = val
    return grid

def island(grid, start):
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
            if neigh in grid and grid[neigh] == grid[current]:
                Q.append(neigh)

    return visited

def calc_perimeter(isle, grid):
    perimeter = 0
    for patch in isle:
        i,j = patch
        neighbors = [(i, j + 1), (i, j - 1), (i + 1, j), (i - 1, j)]
        for neigh in neighbors:
            if neigh not in grid or grid[neigh] != grid[patch]:
                perimeter += 1
    return perimeter

def part_one(islands, grid):
    price = 0
    for isle in islands:
        area = len(isle)
        peri = calc_perimeter(isle, grid)
        price += area * peri

    return price


def getallislands(grid):

    islands = []
    checked = set()

    for point in grid:
        if point not in checked:
            isle = island(grid, point)
            for pt in isle:
                checked.add(pt)
            islands.append(isle)
    return islands

def count_sides(islands, grid):
    def different(this, other, grid):
        if other not in grid or thi not in grid:
            return True
        elif grid[this] != grid[other]:
            return True
        return False

    total = 0
    sorted_points = sorted(island)


grid = create_grid((get_data('real_input.txt')))
isle1 = island(grid,(0,1))
islands = getallislands(grid)
part_one_answer =part_one(islands, grid)






