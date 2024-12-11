# ---Opening Data---
# Open data and strip out newlines

def get_data(file):
    with open(file, encoding='utf-8') as f:
        data = f.read()
        inputs = data.split('\n\n')
    return inputs


answers = get_data("Day6Input.txt")

# ---Part One---
print("Part One:", sum(len(set.union(*map(set, answer.split('\n'))))
                       for answer in answers))

# ---Part Two---
print("Part Two:", sum(len(set.intersection(*map(set, answer.split('\n'))))
                       for answer in answers))
