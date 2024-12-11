
def get_data(file):
    data=[]

    with open(file, 'r') as f:
        input = f.read()



    return input

def prepare_data(rawdata):
    input_rules, input_updates = rawdata.split('\n\n')
    updates_array = [list(row.split(",")) for row in input_updates.splitlines()]
    rules_list_array = [list(row.split("|")) for row in input_rules.splitlines()]
    # convert updates array to int
    updates_array = [[int(value) for value in row] for row in updates_array]

    return updates_array, rules_list_array

def create_rules_dict(rules_list_array):

    rules_dict={}

    for rule in rules_list_array:
        if int(rule[0]) not in rules_dict.keys():
            rules_dict[int(rule[0])] = []
            rules_dict[int(rule[0])].append(int(rule[1]))
        elif int(rule[0]) in rules_dict.keys():
            rules_dict[int(rule[0])].append(int(rule[1]))

    return rules_dict

def check_update(rules_dict, updates_array):

    for page in updates_array:
        if page in rules_dict.keys():
            order_array = rules_dict[page]
            for rule in order_array:
                if rule in updates_array:
                    if updates_array.index(page) > updates_array.index(rule):
                        return False

    return True

def fix_update(rules_dict, updates_array):
    while not check_update(rules_dict, updates_array):
        for page in updates_array:
            if page in rules_dict.keys():
                order_array = rules_dict[page]
                for rule in order_array:
                    if rule in updates_array:
                        if updates_array.index(page) > updates_array.index(rule):
                            updates_array[updates_array.index(page)], updates_array[updates_array.index(rule)] = updates_array[updates_array.index(rule)], updates_array[updates_array.index(page)]
    return updates_array


def part_one():

    problem_input = get_data('input.txt')
    updates = prepare_data(problem_input)[0]
    rules = prepare_data(problem_input)[1]
    rules_dict = create_rules_dict(rules)
    result = 0

    for up in updates:
        if check_update(rules_dict,up):
            result += up[len(up) //2]

    return result

def part_two():

    problem_input = get_data('input.txt')
    updates = prepare_data(problem_input)[0]
    rules = prepare_data(problem_input)[1]
    rules_dict = create_rules_dict(rules)
    result = 0

    for up in updates:
        if not check_update(rules_dict,up):
            up = fix_update(rules_dict, up)
            result += up[len(up) //2]

    return result

print(part_one())
print(part_two())



