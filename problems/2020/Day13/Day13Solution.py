def get_data(file):
    with open(file, 'r') as f:
        my_time = int(f.readline().strip('\n'))
        bus_schedule = [(bus_ID, int(bus)) for bus_ID, bus in enumerate(
            f.readline().split(',')) if bus != 'x']
    return my_time, bus_schedule


def part_one(my_time, bus_schedule):

    wait_time, bus = min([(bus - my_time % bus, bus)
                          for _, bus in bus_schedule])

    return wait_time * bus


print("Part One:", part_one(get_data('Day13Input.txt')
                            [0], get_data('Day13Input.txt')[1]))


def part_two(bus_schedule):

    timestamp, step = 0, 1

    for bus_ID, bus_time in bus_schedule:

        while (timestamp + bus_ID) % bus_time != 0:
            timestamp += step

        step *= bus_time

    return timestamp


print('Part Two:', part_two(get_data('Day13Input.txt')[1]))
