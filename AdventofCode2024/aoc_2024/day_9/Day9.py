#get raw data with minimal processing
def get_data(file):

    #create a list of files and empty space allocations
    with open(file) as f:
        disk_map = list("".join(x.strip() for x in f))

    return disk_map

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

diskmap = get_data('Day9Input.txt')
result = part_one(diskmap)
print(result)

