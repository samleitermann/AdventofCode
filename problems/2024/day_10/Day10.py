def get_data(file):
    # create a list of files and empty space allocations
    with open(file) as f:
        topo_map = [[int(i) for i in x.strip()] for x in f]
    return topo_map

topo_map = get_data("Day10Input.txt")
bounds = len(topo_map)

def follow_trail(x, y, curr, visited, part_1):
    if curr ==9:
        if not part_1:
            return 1
        if (x,y) not in visited:
            visited.add((x,y,))
            return 1
        return 0
    result = 0
    for nx, ny in [(x+1,y), (x-1,y), (x,y+1), (x,y-1)]:
        if 0 <= nx < bounds and 0 <= ny < bounds:
            height = topo_map[ny][nx]
            if height == curr + 1:
                result += follow_trail(nx, ny, height, visited, part_1)
    return result

for part_1 in [True, False]:
    result = 0
    for y, contour in enumerate(topo_map):
        for x, i in enumerate(contour):
            if i==0:
                result += follow_trail(x, y, i, set(), part_1)

    print(result)