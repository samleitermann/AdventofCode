import time

#get raw data with minimal processing
def get_data_one(file):

    #create a list of files and empty space allocations
    with open(file) as f:
        disk_map1 = list("".join(x.strip() for x in f))

    return disk_map1

def get_data_two(file):
    # create a list of files and empty space allocations
    with open(file) as f:
        disk_map2 = [int(i) for i in "".join(x.strip() for x in f)]
    return disk_map2

def part_one(disk_map):
    expanded_data = []

    for i, r in enumerate(disk_map):
        if i %2 == 0:
            for k in range(int(r)):
                expanded_data.append(f'{i//2}')

        else:
            for k in range(int(r)):
                expanded_data.append('.')

    pointer = 0
    end_pointer = len(expanded_data) -1

    while pointer < end_pointer:
        while expanded_data[pointer] != ".":
            pointer += 1
        while expanded_data[end_pointer] == ".":
            end_pointer -= 1

        expanded_data[pointer] = expanded_data[end_pointer]
        expanded_data[end_pointer] = "."

        pointer += 1
        end_pointer -= 1

    compacted_data = [c for c in expanded_data if c!= '.']
    result = sum(i*int(c) for i,c in enumerate(compacted_data))

    return result

def part_two(disk_map):

    data_map = {}
    free_space = []

    count = 0

    for i, r in enumerate(disk_map):
        start,end = count, count+r
        if i % 2 == 0:
            data_map[i//2] = (start,end)
        elif r>0:
            free_space.append((start,end))
        count += r

    index_pointer = max(data_map.keys())

    while index_pointer >= 0:
        fstart, fend = data_map[index_pointer]
        flen = fend - fstart

        free_pointer = 0
        while free_pointer < len(free_space):
            gstart, gend = free_space[free_pointer]
            if gstart >= fstart:
                break

            glen = gend - gstart
            if flen <= glen:
                free_space.pop(free_pointer)

                new_fstart , new_fend = gstart, gstart+flen
                new_gstart, new_gend = new_fend, gend

                data_map[index_pointer] = (new_fstart, new_fend)
                if new_gstart != new_gend:
                    free_space.insert(free_pointer, (new_gstart, new_gend))
                break
            else:
                free_pointer += 1

        index_pointer -= 1

    result = 0
    for k, (start,end) in data_map.items():
        result += sum(k*i for i in range(start,end))

    return result


start = time.perf_counter()

diskmap1 = get_data_one('Day9Input.txt')
result1 = part_one(diskmap1)

diskmap2 = get_data_two('Day9Input.txt')
result2 = part_two(diskmap2)

print('Part One: ', result1)
print('Part Two: ', result2)

end = time.perf_counter()

print("Time taken to execute: ", end-start, ' seconds')