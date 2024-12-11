
def get_data(file):
    data=[]


    #open the file and strip out trailing whitespace

    with open(file, 'r') as f:
        for line in f:
            data.append(line.strip())

    return data

def part_one(data):

    lines = []


    for l in data:
        lines.append(list(l))

    #Create arrays for diagonal and anti-diagonal lines and also invert all lines.
    diagonal = [[] for d in range(len(lines) + len(lines[0])-1)]
    antidiagonal = [[] for ad in range(len(diagonal))]
    transpose = list(zip(*lines))

    #because each anti-diagonal consists of elements where x-y is constant, and because x-y will be negative for half
    #the grid, we create a value to shift all the indices up by the largest negative value of x-y (assuming more rows than columns
    #to make sure we don't have that occur.
    min_antidiagonal = -len(lines)+1

    for y, row in enumerate(lines):
        for x, val in enumerate(row):
            diagonal[x+y].append(val)
            antidiagonal[x-y-min_antidiagonal].append(val)

    result = 0

    for line in lines + diagonal + antidiagonal + transpose:
        line = ''.join(line)
        result += line.count('XMAS') + line.count('SAMX')

    return result


print(part_one(get_data('input.txt')))

def part_two(data):

    result = 0

    for i, line in enumerate(data[1:-1], start = 1):
        for j, val in enumerate(line[1:-1], start = 1):
            if val != 'A':
                continue
            patterns = alid = ['MSMS', 'SMSM', 'SMMS', 'MSSM']
            if data[i-1][j-1]+data[i+1][j+1]+data[i+1][j-1]+data[i-1][j+1] in patterns:
                result += 1

    return result

print(part_two(get_data('input.txt')))



