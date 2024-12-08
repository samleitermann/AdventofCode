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

def find_antinodes(antenna, antennas):
    #returns all possible antinodes given a combination of two antenna locations in my dictionary
    return [(2*x1-x2,2*y1-y2) for (x1,y1),(x2,y2) in itertools.permutations(antennas[antenna],2)]

#checks to see if the nodes I've listed are valid. If so, returns a list of those nodes.
def check_nodes(anti_nodes, x_len, y_len):

    valid_nodes = []

    for anti_node in anti_nodes:
        if 0 <= anti_node[0] < x_len and 0 <= anti_node[1] < y_len and anti_node not in valid_nodes:
            valid_nodes.append(anti_node)

    return valid_nodes

start = time.perf_counter()
raw = get_data('Day8Input.txt')
antennas = parse_data(raw)
anti_nodes = [find_antinodes(antenna, antennas) for antenna in antennas]
anti_nodes = [x for l in anti_nodes for x in l]
num_nodes = len(check_nodes(anti_nodes,len(raw), len(raw[0])))
print(f'{'Part One: '}{num_nodes}')
end = time.perf_counter()

print("Time taken to execute: ", end-start, ' seconds')