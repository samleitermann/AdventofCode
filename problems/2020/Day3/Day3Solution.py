def get_data(file):
    with open(file, 'r') as f:
        data = [line.strip() for line in f]
    return data


terrain = get_data("Day3Input.txt")

# set parameters for [right, down, position, step, trees_hit]
directions = [[1, 1, 0, 1, 0], [3, 1, 0, 1, 0], [
    5, 1, 0, 1, 0], [7, 1, 0, 1, 0], [1, 2, 0, 1, 0]]

# Function to count collisions


def collision_count(in_terrain, map_length, direction):
    # set the parameters
    right = direction[0]
    down = direction[1]
    position = direction[2]
    tree_crash = direction[4]

    # need to count lines to skip lines when our slope becomes non-integer
    line_count = 0

    # loop through terrain and then (1) check if we're on an appropriate line for the slope,
    # (2) check if we've hit a tree, and (3) check our position and loop back in the line if necessary.
    for terr in in_terrain:
        # check that we've moved down far enough.
        if line_count % down == 0:
            # check if we've hit a tree
            if terr[position % map_length] == '#':

                tree_crash += 1

            position += right

        line_count += 1

    return(tree_crash)

# function to run over multiple paths and multiply.


def part_two(in_terrain, directions):
    # count the number of times to run part_one and add a product variable to calculate the product
    count = 0
    product = 1

    # loop through part one with different parameters
    for direction in directions:
        product *= collision_count(in_terrain,
                                   len(in_terrain[0]), directions[count])
        count += 1

    # for i in range(count):
        #product = product*temp_directions[i][4]

    return(product)


print("Part One:", collision_count(terrain, len(terrain[0]), directions[1]))
print("Part Two:", part_two(terrain, directions))
