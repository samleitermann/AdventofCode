import time

from itertools import cycle

#define constants that we need to have.

GUARD = '^'
OBJECT = '#'
FLOOR = '.'

UP = (-1, 0)
RIGHT = (0, 1)
DOWN = (1, 0)
LEFT = (0, -1)

#get raw data with minimal processing
def get_data(file):

    #open the file and strip out trailing whitespace

    with open(file, 'r') as f:
        rawdata = f.read()
        data = [list(row) for row in rawdata.splitlines()]

    return data

def parse_data(data):

#create a dictionary with each grid point and its current status.

    parsed_map = {}
    raw_map = data
    guard = None

    for i in range(len(raw_map)):
        for j in range(len(raw_map[0])):
            current = raw_map[i][j]
            if current == GUARD:
                guard = (i, j)
                parsed_map[(i, j)] = FLOOR
            else:
                parsed_map[(i, j)] = current
    return guard, parsed_map

def step(guard, direction):
    i, j = guard
    di, dj = direction

    return(i + di, j + dj)

def facing_wall(guard, direction, lab_map):
    i,j = guard
    di, dj = direction
    future_step = (i+di, j+dj)
    if lab_map[future_step] == OBJECT:
        return True
    return False

def future_step_in_map(guard, direction, lab_map):
    i, j = guard
    di, dj = direction
    future_step = (i + di, j + dj)
    return future_step in lab_map

def guard_simulation(guard, lab):
    DIRECTIONS = cycle([UP, RIGHT, DOWN, LEFT])
    future_dir = next(DIRECTIONS)
    visited = set()
    visited_cycle = set()
    path_is_cycle = False

    while True:
        visited.add(guard)
        if (guard,future_dir) in visited_cycle:
            path_is_cycle = True
            break
        else:
            visited_cycle.add((guard, future_dir))

        if not future_step_in_map(guard, future_dir, lab):
            break
        elif facing_wall(guard, future_dir, lab):
            future_dir = next(DIRECTIONS)
        else:
            guard = step(guard, future_dir)

    return visited, path_is_cycle

def find_obstacles(guard, lab):
    possible_obstacles, _ = guard_simulation(guard, lab)
    possible_obstacles.remove(guard)

    obstacles = set()

    for option in possible_obstacles:
        changed_lab = lab.copy()
        changed_lab[option] = OBJECT
        _ , is_cycle = guard_simulation(guard, changed_lab)
        if is_cycle:
            obstacles.add(option)

    return obstacles


guard, lab = parse_data(get_data('Day6Input.txt'))
start = time.perf_counter()
print('Part One: ', len(guard_simulation(guard,lab)[0]))
print('Part Two: ', len(find_obstacles(guard, lab)))
end = time.perf_counter()

print('Time Taken = ', end-start)





