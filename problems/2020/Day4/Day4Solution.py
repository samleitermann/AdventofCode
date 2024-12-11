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
part_two = 0


# ---Taking List to Dict---

for index, i in enumerate(passport_input):
    rawdata = i.replace('\n', ' ').split()
    details = [i.split(':') for i in rawdata]
    passport_dict = {x[0]: x[1] for x in details}
    passports.append(passport_dict)

# ---Counting Valid Passports for Part One---

#print("Part One:", part_one)

# ---Validation Functions--- (Each function validates one of the fields)


def byr_validation(byr_pass):
    return len(byr_pass) == 4 and int(byr_pass) <= 2002 and int(byr_pass) >= 1920


def iyr_validation(iyr_pass):
    return len(iyr_pass) == 4 and int(iyr_pass) <= 2020 and int(iyr_pass) >= 2010


def eyr_validation(eyr_pass):
    return len(eyr_pass) == 4 and int(eyr_pass) <= 2030 and int(eyr_pass) >= 2020


def hgt_validation(hgt_pass):
    if hgt_pass[-2:] == 'cm':
        return int(hgt_pass[:-2]) >= 150 and int(hgt_pass[:-2]) <= 193
    if hgt_pass[-2:] == 'in':
        return int(hgt_pass[:-2]) >= 59 and int(hgt_pass[:-2]) <= 76


def hcl_validation(hcl_pass):
    return hcl_pass[0] == '#' and len(hcl_pass[1:]) == 6 and hcl_pass[1:].isalnum()


def ecl_validation(ecl_pass):
    return ecl_pass in ['amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth']


def pid_validation(pid_pass):
    return len(pid_pass) == 9


def cid_validation(cid_pass):
    return 0


def validation_passport(passport):
    # returns true if all validations are correct.
    return all([byr_validation(passport['byr']), iyr_validation(passport['iyr']), eyr_validation(passport['eyr']),
    hgt_validation(passport['hgt']), hcl_validation(passport['hcl']), ecl_validation(passport['ecl']), pid_validation(passport['pid'])])


for index, passport in enumerate(passports):
    # which keys are present.AssertionError
    keys = passport.keys()
    # check to make sure all fields are present.
    if all(field in keys for field in fields):
        part_one += 1
        # check to see all the fields are valid.
        if validation_passport(passport):
            part_two += 1


print("Part One:", part_one)
print("Part Two:", part_two)
