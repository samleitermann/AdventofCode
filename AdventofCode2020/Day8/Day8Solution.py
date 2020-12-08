def get_data(file) -> list:
    with open(file, 'r') as f:
        file_list = f.read().splitlines()
        for ind, ins in enumerate(file_list):
            file_list[ind] = [ins[:3], int(ins[4:])]
    return file_list


instr = get_data('Day8Input.txt')


def part_one(instructions):
    seen = {}
    accumulator = 0
    instr_index = 0

    while True:

        if instr_index in seen:
            return accumulator

        ins = instructions[instr_index][0]

        if ins == 'nop':
            seen[instr_index] = True
            instr_index += 1

        elif ins == 'jmp':
            seen[instr_index] = True
            instr_index += instructions[instr_index][1]

        elif ins == 'acc':
            seen[instr_index] = True
            accumulator += instructions[instr_index][1]
            instr_index += 1


def part_two(instructions):
    seen = {}
    accumulator = 0
    instr_index = 0

    for item in range(len(instructions)):
        new_instructions = get_data("Day8Input.txt")

        if new_instructions[item][0] == 'jmp':
            new_instructions[item][0] = 'nop'
        elif new_instructions[item][0] == 'nop':
            new_instructions[item][0] = 'jmp'

        seen = {}
        accumulator = 0
        instr_index = 0

        while True:

            ins = new_instructions[instr_index][0]

            if ins == 'nop':
                seen[instr_index] = True
                instr_index += 1

            elif ins == 'jmp':
                seen[instr_index] = True
                instr_index += instructions[instr_index][1]

            elif ins == 'acc':
                seen[instr_index] = True
                accumulator += instructions[instr_index][1]
                instr_index += 1

            if instr_index in seen:
                break

            if instr_index == len(new_instructions) - 1:
                if new_instructions[instr_index][0] == 'acc':
                    accumulator += new_instructions[instr_index][1]
                return accumulator


print('Part One:', part_one(instr))
print('Part Two:', part_two(instr))
