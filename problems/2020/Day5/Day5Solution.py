# ---Open Data---
def get_data(file):
    with open(file, 'r') as f:
        data = [line.strip() for line in f]
    return data


seats = get_data("Day5Input.txt")

# ---Initialize Empty Array for Seat Codes---
seat_codes = []

# ---Realize this is just a binary representation and converty
for seat in seats:
    seat_codes.append(int(seat.replace("F", "0").replace(
        "B", "1").replace("L", "0").replace("R", '1'), 2))

# ---Solve for part one by finding max
part_one = max(seat_codes)

# ---Do a set minus by looking at all seats that are one more and all that are one less
#    and subtracting the original set---

my_seat = (set([x + 1 for x in seat_codes]) &
           set(x - 1 for x in seat_codes)) - set(seat_codes)

print("Part One:", part_one)
print("Part Two:", my_seat)
