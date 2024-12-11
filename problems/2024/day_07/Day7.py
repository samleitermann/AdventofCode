import re, time

#get raw data with minimal processing
def get_data(file):

    #open the file create a list with the test value as the first value and the values to be
    #combined as the rest of the values. Use regular expressions to split in a more complex way.
    with open(file, 'r') as f:
        data = [list(map(int, re.split(r': | ', line.strip()))) for line in f.readlines()]

    return data

#Initializes the recursion loop and returns the value if it results in a true statement or returns 0 if not.
def parse_data(dat):
    test_val = dat[0]
    start_val = dat[1]
    remaining_vals = dat[2:]

    if op_deter(test_val, start_val, remaining_vals):
        return test_val
    else:
        return 0

#Recursion loop: check if there are no more numbers to use, check if we've actually reached our target. Test if we've overshot our value, and then if not recurs
#to check the set of expressions again. Allows for faster code because the moment we've been unsuccessful we exit. Only needs a slight modification for part 2
#to allow for concatenation.
def op_deter(test_val, current_val, remaining_vals):

    #check if we've run out of numbers and whether we've reached the test value
    if len(remaining_vals) == 0:
        return current_val == test_val

    #check if we've exceeded our test value
    if current_val > test_val:
        return False

    #set the next value as well as the values that are left.
    nxt = remaining_vals[0]
    remaining_vals = remaining_vals[1:]

    #don't include concatenation if you're doing part one.
    #return (op_deter(test_val, current_val + nxt, remaining_vals) or op_deter(test_val, current_val * nxt, remaining_vals))
    return (op_deter(test_val, current_val + nxt, remaining_vals) or
            op_deter(test_val, current_val * nxt, remaining_vals) or
            op_deter(test_val, int(f'{current_val}{nxt}'), remaining_vals))

start = time.perf_counter()
#print("Part One: ", sum(parse_data(d) for d in get_data('input.txt')))
print("Part Two: ", sum(parse_data(d) for d in get_data('input.txt')))
end = time.perf_counter()

print("Time taken to execute: ", end-start, ' seconds')