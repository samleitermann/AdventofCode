def get_data(file):
    with open(file, 'r') as f:
        data = [line.strip() for line in f]
    return data

terrain = get_data("Day3Input.txt")

#set parameters for [right, down, position, step, trees_hit]
directions = [[1, 1, 0, 1, 0],[3, 1, 0, 1, 0],[5, 1, 0, 1, 0],[7, 1, 0, 1, 0],[1, 2, 0, 1, 0]]

#part one

def part_one(in_terrain, map_length, direction):
    #set the parameters
    right = direction[0]
    down = direction[1]
    position = direction[2]

    #need to count lines to skip lines when our slope becomes non-integer
    line_count = 0

    #loop through terrain and then (1) check if we're on an appropriate line for the slope, (2) check if we've hit a tree, and (3) check our position and loop back in the line if necessary.
    for terr in in_terrain:
        #check that we've moved down far enough.
        if line_count % down == 0:
            #check if we've hit a tree
            if terr[position] == '#':
                direction[4] += 1


        #if we won't hit the end of the line, great!
        if (position+right) < (map_length - 1):
            position += right
            #if we do hit the end of the line, loop us back to the beginning and restart.
        else:
            position = position - map_length + right
            #note that we have moved down a line
        line_count += 1


        return(direction[4])

#solution to part one (Moved to bottom to not be dumb)
#print("Part One:", part_one(terrain, len(terrain[0]), directions[1]))

def part_two(in_terrain,directions):
    #count the number of times to run part_one and add a product variable to calculate the product
    count = 0
    product = 1

    temp_directions = directions

    #loop through part one with different parameters
    for direction in temp_directions:
        part_one(in_terrain,len(in_terrain[0]),temp_directions[count])
        count +=1

    for i in range(count):
        product = product*temp_directions[i][4]

    return(temp_directions[1][4],product)

print("Answers:", part_two(terrain,directions))


#Should really just make it so the function makes a copy of the data and thus doesn't modify the original directions file. That would be better. Not going to right now.
