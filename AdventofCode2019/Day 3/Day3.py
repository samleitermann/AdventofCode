A,B= open('Day3Input.txt').read().splitlines()
A,B = [x.split(',') for x in [A,B]]

DictX = {"U":0, "D": 0, "L":-1, "R":1}
DictY = {"U":1, "D":-1, "L":0, "R":0}

def points(A):
    x = 0
    y = 0
    length = 0
    ans = {}
    for cmd in A:
        direction = cmd[0]
        distance = int(cmd[1:])

        for _ in range(distance):
            x += DictX[direction]
            y += DictY[direction]
            length += 1
            if (x,y) not in ans:
                ans[(x,y)] = length
    return ans

PA = points(A)
PB = points(B)

both = set(PA.keys())&set(PB.keys())
part1 = min([abs(x)+abs(y) for (x,y) in both])
part2 = min([PA[p]+PB[p] for p in both])

print(part2)
