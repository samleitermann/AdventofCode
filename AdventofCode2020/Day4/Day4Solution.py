# ---Opening Data---
# Open data and strip out newlines

def get_data(file):
    with open(file, encoding='utf-8') as f:
        data = f.read()
        inputs = data.split('\n\n')
    return inputs


# ---Fetching Data and Defining Variables---
# fetch data and initialize passport array, define fields and
passport_input = get_data("Day4Input.txt")

passports = []

fields = ['byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid', 'cid']
fields.remove('cid')

part_one = 0


# ---Taking List to Dict---

for index, i in enumerate(passport_input):
    rawdata = i.replace('\n', ' ').split()
    details = [i.split(':') for i in rawdata]
    passport_dict = {x[0]: x[1] for x in details}
    passports.append(passport_dict)

# ---Counting Valid Passports for Part One---

for index, passport in enumerate(passports):
    keys = passport.keys()
    if all(field in keys for field in fields):
        part_one += 1

print("Part One:", part_one)
