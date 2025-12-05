input_path = "day5.txt"

def brute_force_part_1():
    validnums = set()
    fresh = 0
    ranges = True
    with open(input_path) as f:
        for row in f:
            if len(row.strip()) == 0:
                ranges = False
            elif ranges:
                rangeends = row.strip().split("-")
                for i in range(int(rangeends[0]), int(rangeends[1]) + 1):
                    validnums.add(i)
            else:
                if int(row.strip()) in validnums:
                    fresh += 1

    return fresh

def read_sorted_lists():
    rangelist = []
    checknums = []
    ranges = True
    with open(input_path) as f:
        for row in f:
            if len(row.strip()) == 0:
                ranges = False
            elif ranges:
                rangeends = row.strip().split("-")
                rangelist.append((int(rangeends[0]),int(rangeends[1])))
            else:
                checknums.append(row.strip())
    return rangelist, checknums

def get_fresh_for_num(sortedranges, num):
    for range in sortedranges:
        if range[0] <= num and range[1] >= num:
            return 1
        if range[0] > num:
            return 0
    return 0

def compute_fresh_part_1(rangelist, checknums):
    sortedranges = sorted(rangelist)
    print("\nDEBUG RANGES: " + str(sortedranges))

    print("\nDEBUG CHECKNUMS: " + str(checknums))

    print("\nDEBUG NUM RANGES : " + str(len(sortedranges)))

    print("\nDEBUG NUM CHECKNUMS : " + str(len(checknums)))
    fresh = 0

    for num in checknums:
        fresh += get_fresh_for_num(sortedranges, int(num))

    return fresh

def collapse_ranges(rangelist):
    for index, range in enumerate(rangelist):
        for previdx, prevrange in enumerate(rangelist[:index]):
                # Starts in previous range
                if prevrange[0] <= range[0] and prevrange[1] >= range[0]:
                    # Ends past other range
                    if range[1] > prevrange[1]:
                        # Collapse this range
                        return rangelist[:previdx] + rangelist[previdx+1:index] + rangelist[index+1:] + [(prevrange[0], range[1])]
                # Ends in previous range
                if prevrange[0] <= range[1] and prevrange[1] >= range[1]:
                    # Starts before other range
                    if range[0] < prevrange[0]:
                        # Collapse this range
                        return rangelist[:previdx] + rangelist[previdx+1:index] + rangelist[index+1:] + [(range[0], prevrange[1])]
                # Contained in previous range
                if prevrange[0] <= range[0] and prevrange[1] >= range[1]:
                    # Delete this range
                    return rangelist[:index] + rangelist[index+1:]
                # Contains a previous range
                if prevrange[0] >= range[0] and prevrange[1] <= range[1]:
                    # Delete that range
                    return rangelist[:previdx] + rangelist[previdx+1:]
    return None

def run_part_2(rangelist):
    has_changes = "some_sentinel"
    while has_changes != None:
        has_changes = collapse_ranges(rangelist)
        if has_changes != None:
            rangelist = has_changes
    
    total_nums = 0
    for range in rangelist:
        total_nums += range[1] - range[0] + 1
    return total_nums


def test_part_2():
    test_range = [(3,5),(10,14),(16,20),(12,18)]
    return run_part_2(test_range)

rangelist, checknums = read_sorted_lists()
print("Part 1 : " + str(compute_fresh_part_1(rangelist, checknums)))

print("Test Part 2 : " + str(test_part_2()))

rangelist, checknums = read_sorted_lists()
print("Part 2 : " + str(run_part_2(rangelist)))
