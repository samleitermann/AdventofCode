#going to look at permutations of coordinates so need this.
import itertools, time

#get raw data with minimal processing
def get_data(file):

    #open the file and strip out trailing whitespace

    with open(file, 'r') as f:
        rawdata = f.read()
        data = [list(row) for row in rawdata.splitlines()]

    return data


def parse_data(data):

#create a dictionary with each grid point (I do not need to do this)
    FLOOR = '.'
    raw_map = data
    antennas = {}

    #Create a dictionary of antennas so I know where they all are.
    for i in range(len(raw_map)):
        for j in range(len(raw_map[0])):
            current = raw_map[i][j]
            if current not in antennas.keys() and current != FLOOR:
                antennas[current] = [(i,j)]
            elif current in antennas.keys():
                antennas[current].append((i,j))

    return antennas

def find_antinodes1(antenna, antennas):
    #returns all possible antinodes given a combination of two antenna locations in my dictionary
    return [(2*x1-x2,2*y1-y2) for (x1,y1),(x2,y2) in itertools.permutations(antennas[antenna],2)]

def find_antinodes2(coords1, coords2, len_x, len_y):
    #set my initial antenna coordinates
    x1, y1 = coords1
    x2, y2 = coords2
    #set the distance that creates anti-nodes on a straight line
    dx = x2-x1
    dy = y2-y1
    #initialize output list
    output = []
    #while loop through anti-node locations going forward and exit when limits of map are reached.
    xcurr, ycurr = x1 , y1
    while 0 <= xcurr <= len_x and 0 <= ycurr <= len_y:
        output.append((xcurr, ycurr))
        xcurr,ycurr = xcurr+dx, ycurr+dy
    # while loop through anti-node locations going backward and exit when limits of map are reached.
    xcurr, ycurr = x1 , y1
    while 0 <= xcurr <= len_x and 0 <= ycurr <= len_y:
        output.append((xcurr, ycurr))
        xcurr,ycurr = xcurr-dx, ycurr-dy

    return output

#checks to see if the nodes I've listed are valid. If so, returns a list of those nodes.
def check_nodes(anti_nodes, x_len, y_len):

    valid_nodes = []
    #check for bounds and duplicates because I was too lazy to do this in part one.
    for anti_node in anti_nodes:
        if 0 <= anti_node[0] < x_len and 0 <= anti_node[1] < y_len and anti_node not in valid_nodes:
            valid_nodes.append(anti_node)

    return valid_nodes

def generate_antinodes_part_2(antennas, raw):
    #initialize an empty list of nodes
    antinodes_2 = []

    #cycle through my pairs of antennas to generate nodes
    for antenna in antennas:
        for (x1,y1),(x2,y2) in itertools.permutations(antennas[antenna],2):
            antinodes_2.append(find_antinodes2((x1,y1),(x2,y2),len(raw),len(raw[0])))

    return antinodes_2

start = time.perf_counter()
#get data
raw = get_data('Day8Input.txt')
#create list of antennas
antennas = parse_data(raw)
#create array of nodes, flatten it, and then check length. (Part One)
anti_nodes = [find_antinodes1(antenna, antennas) for antenna in antennas]
anti_nodes = [x for l in anti_nodes for x in l]
num_nodes = len(check_nodes(anti_nodes,len(raw), len(raw[0])))
#create array of nodes, flatten it, and then check length. (Part Two)
anti_nodes2 = generate_antinodes_part_2(antennas, raw)
anti_nodes2 = [x for l in anti_nodes2 for x in l]
num_nodes2 = len(check_nodes(anti_nodes2,len(raw), len(raw[0])))
#Print Solutions
print(f'{'Part One: '}{num_nodes}')
print(f'{'Part Two: '}{num_nodes2 }')
end = time.perf_counter()

print("Time taken to execute: ", end-start, ' seconds')