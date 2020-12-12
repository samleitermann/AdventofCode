def get_data(file):
    with open(file, encoding='utf-8') as f:
        data = f.read()
        inputs = data.split('\n')
    return inputs


seats = get_data("Day11Input.txt")

# Create a Seat class that can hold the information about a seat.


class Seat():
    def __init__(self):
        self.occupied = False
        self.occupied_next = False
        self.neighbors = []

# Get the neighbors of any given seat


def hey_there_hi_there(seatmap, y_pos, x_pos):

    neighberino = []

    possibles = [(y_pos - 1, x_pos - 1), (y_pos - 1, x_pos), (y_pos - 1, x_pos + 1), (y_pos, x_pos + 1),
                 (y_pos + 1, x_pos + 1), (y_pos + 1, x_pos), (y_pos + 1, x_pos - 1), (y_pos, x_pos - 1)]

    for possible in possibles:
        # check to see if the seats are in bounds and if its not floor.
        if possible[0] >= 0 and possible[0] < len(seatmap) and possible[1] >= 0 and possible[1] < len(seatmap[0]) and seatmap[possible[0]][possible[1]] != None:
            # add as a possible seat
            neighberino.append(possible)

    return neighberino


def map_it(seats):

    seatmap = []

    for line in seats:
        map_line = []
        for seat in line:
            if seat == 'L':
                map_line.append(Seat())
            else:
                map_line.append(None)

        seatmap.append(map_line)

    return seatmap


def part_one(seatmap):

    for i in range(len(seatmap)):
        for j in range(len(seatmap[0])):
            if seatmap[i][j] != None:
                seatmap[i][j].neighbors = hey_there_hi_there(seatmap, i, j)

    changed = True

    while changed:
        changed = False
        for i in range(len(seatmap)):

            for j in range(len(seatmap[0])):

                if seatmap[i][j] != None:

                    current_seat = seatmap[i][j]

                    if seatmap[i][j].occupied == False:
                        adjacent_occupied = 0
                        for adjacent_seat_pos in seatmap[i][j].neighbors:
                            adjacent_seat = seatmap[adjacent_seat_pos[0]
                                                    ][adjacent_seat_pos[1]]
                            if adjacent_seat == None:
                                adjacent_occupied += 0
                            elif adjacent_seat.occupied:
                                adjacent_occupied += 1
                        if adjacent_occupied == 0:
                            changed = True
                            seatmap[i][j].occupied_next = True
                        else:
                            seatmap[i][j].occupied_next = False
                    else:
                        adjacent_occupied = 0
                        for adjacent_seat_pos in seatmap[i][j].neighbors:
                            adjacent_seat = seatmap[adjacent_seat_pos[0]
                                                    ][adjacent_seat_pos[1]]
                            if adjacent_seat == None:
                                adjacent_occupied += 0
                            elif adjacent_seat.occupied:
                                adjacent_occupied += 1
                        if adjacent_occupied >= 4:
                            changed = True
                            seatmap[i][j].occupied_next = False
                        else:
                            seatmap[i][j].occupied_next = True

        for i in range(len(seatmap)):
            for j in range(len(seatmap[0])):
                if seatmap[i][j] != None:
                    seatmap[i][j].occupied = seatmap[i][j].occupied_next

    total_occupied = 0

    for i in range(len(seatmap)):

        for j in range(len(seatmap[0])):

            if seatmap[i][j] != None and seatmap[i][j].occupied == True:
                total_occupied += 1

    return total_occupied


print('Part One:', part_one(map_it(seats)))

# Part Two
# get neighbors for new problem


def hey_there_hi_there_ho_there(seatmap, y_pos, x_pos):
    neighbors = []

    # Up
    for i in range(1, len(seatmap)):
        if (y_pos - i) >= 0 and seatmap[y_pos - i][x_pos] != None:
            neighbors.append((y_pos - i, x_pos))
            break

    # Up right
    for i in range(1, len(seatmap[0])):
        if (y_pos - i) >= 0 and (x_pos + i) < len(seatmap[0]) and seatmap[y_pos - i][x_pos + i] != None:
            neighbors.append((y_pos - i, x_pos + i))
            break

    # Right
    for i in range(1, len(seatmap[0])):
        if (x_pos + i) < len(seatmap[0]) and seatmap[y_pos][x_pos + i] != None:
            neighbors.append((y_pos, x_pos + i))
            break

    # Down Right
    for i in range(1, len(seatmap) + len(seatmap[0])):
        if (y_pos + i) < len(seatmap) and (x_pos + i) < len(seatmap[0]) and seatmap[y_pos + i][x_pos + i] != None:
            neighbors.append((y_pos + i, x_pos + i))
            break

    # Down
    for i in range(1, len(seatmap)):
        if (y_pos + i) < len(seatmap) and seatmap[y_pos + i][x_pos] != None:
            neighbors.append((y_pos + i, x_pos))
            break

    # Down Left
    for i in range(1, len(seatmap)):
        if (y_pos + i) < len(seatmap) and (x_pos - i) >= 0 and seatmap[y_pos + i][x_pos - i] != None:
            neighbors.append((y_pos + i, x_pos - i))
            break

    # Left
    for i in range(1, len(seatmap)):
        if (x_pos - i) >= 0 and seatmap[y_pos][x_pos - i] != None:
            neighbors.append((y_pos, x_pos - i))
            break

    # Up Left
    for i in range(1, len(seatmap)):
        if (y_pos - i) >= 0 and (x_pos - i) >= 0 and seatmap[y_pos - i][x_pos - i] != None:
            neighbors.append((y_pos - i, x_pos - i))
            break

    return neighbors


def part_two(seatmap):

    for i in range(len(seatmap)):
        for j in range(len(seatmap[0])):
            if seatmap[i][j] != None:
                seatmap[i][j].neighbors = hey_there_hi_there_ho_there(
                    seatmap, i, j)

    changed = True

    while changed:
        changed = False
        for i in range(len(seatmap)):

            for j in range(len(seatmap[0])):

                if seatmap[i][j] != None:

                    current_seat = seatmap[i][j]

                    if seatmap[i][j].occupied == False:
                        adjacent_occupied = 0
                        for adjacent_seat_pos in seatmap[i][j].neighbors:
                            adjacent_seat = seatmap[adjacent_seat_pos[0]
                                                    ][adjacent_seat_pos[1]]
                            if adjacent_seat == None:
                                adjacent_occupied += 0
                            elif adjacent_seat.occupied:
                                adjacent_occupied += 1
                        if adjacent_occupied == 0:
                            changed = True
                            seatmap[i][j].occupied_next = True
                        else:
                            seatmap[i][j].occupied_next = False
                    else:
                        adjacent_occupied = 0
                        for adjacent_seat_pos in seatmap[i][j].neighbors:
                            adjacent_seat = seatmap[adjacent_seat_pos[0]
                                                    ][adjacent_seat_pos[1]]
                            if adjacent_seat == None:
                                adjacent_occupied += 0
                            elif adjacent_seat.occupied:
                                adjacent_occupied += 1
                        if adjacent_occupied >= 5:
                            changed = True
                            seatmap[i][j].occupied_next = False
                        else:
                            seatmap[i][j].occupied_next = True

        for i in range(len(seatmap)):
            for j in range(len(seatmap[0])):
                if seatmap[i][j] != None:
                    seatmap[i][j].occupied = seatmap[i][j].occupied_next

    total_occupied = 0

    for i in range(len(seatmap)):

        for j in range(len(seatmap[0])):

            if seatmap[i][j] != None and seatmap[i][j].occupied == True:
                total_occupied += 1

    return total_occupied


print("Part Two:", part_two(map_it(seats)))
