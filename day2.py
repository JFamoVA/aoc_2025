def is_number_invalid(num):
    numstr = str(num)
    # Only works in part 1
    # if len(numstr) % 2 != 0:
    #     return False
    halfway_idx = int(len(numstr) / 2)
    if numstr[:halfway_idx] == numstr[halfway_idx:]:
        return True
    # for substrlen in range(1, halfway_idx):
    #     if is_number_invalid(numstr[substrlen:]):
    #         return True
    return False

input_path = "day2.txt"

def read_input():
    with open(input_path) as f:
        for line in f:
            ranges = line.split(",")
            for range in ranges:
                range_idxs = range.split("-")
                yield int(range_idxs[0]), int(range_idxs[1])

def is_number_invalid_many_times(num):
    numstr = str(num)

    # Even is easy
    halfway_idx = int(len(numstr) / 2)
    if numstr[:halfway_idx] == numstr[halfway_idx:]:
        return True

    # For odd, use a sort of two pointers
    firstchar = numstr[0]
    nextfirstchar_idx = len(numstr)

    search_start_idx = 1

    while nextfirstchar_idx > 0 and search_start_idx <= halfway_idx:
        nextfirstchar_idx = numstr.find(firstchar, search_start_idx)
        if nextfirstchar_idx < 0:
            break
        teststr = numstr[0:nextfirstchar_idx]
        if is_string_only_substring(numstr, teststr):
            return True
        search_start_idx += 1
    
    return False

def is_string_only_substring(mainstr, substr):
    checkstr = mainstr.replace(substr, "")
    return len(checkstr) == 0

def run_part_1():

    invalid_sum = 0

    for range_pair in read_input():
        for i in range(range_pair[0], range_pair[1]+1):
            if is_number_invalid(i):
                invalid_sum += i

    return invalid_sum

def run_part_2():

    invalid_sum = 0

    for range_pair in read_input():
        for i in range(range_pair[0], range_pair[1]+1):
            if is_number_invalid_many_times(i):
                invalid_sum += i

    return invalid_sum

print("Part 1 Result " + str(run_part_1()))
print("Part 2 Result " + str(run_part_2()))