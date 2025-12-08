import math


input_path = "day6.txt"

def read_input_part_1():
    with open(input_path) as f:
        rows = []
        for row in f:
            entries = row.split()
            rows.append(entries)
    return rows

def test_input_format():
    rows = read_input_part_1()
    print("Total rows: " + str(len(rows)))
    for row in rows:
        print("Reading row with length: " + str(len(row)))

def perform_operation(op, nums):
    if op == "+":
        return sum(nums)
    elif op == "*":
        return math.prod(nums)

def run_part_1():
    total = 0

    rows = read_input_part_1()
    for col in range(len(rows[0])):
        op = rows[-1][col]
        total += perform_operation(op, [int(row[col]) for row in rows[:-1]])
    
    return total


def read_input_part_2():
    line_length = 0
    lines = 0
    with open(input_path) as f:
        for line in f:
            line_length = len(line.strip("\n"))
            lines += 1

    grid = [[" " for i in range(line_length)] for j in range(lines)]

    print("Created " + str(line_length) + " x " + str(lines) + " grid")

    with open(input_path) as f:
        for ridx, row in enumerate(f):
            for cidx, char in enumerate(row.strip("\n")):
                try:
                    grid[ridx][cidx] = char
                except IndexError:
                    print(f"DEBUG: trying to write to grid at {ridx}, {cidx}")

    print(f"DEBUG: Producing grid with dimensions {len(grid)} x [{len(grid[0])}, {len(grid[1])}, {len(grid[2])}, {len(grid[3])}, {len(grid[4])}]")

    return grid

def run_part_2():
    grid = read_input_part_2()
    total = 0
    problem_nums = []
    # Go backwards through each col in the grid
    for i in range(len(grid[0])-1, -1, -1):
        # Calculate the number
        numstr = ""
        for numrow in grid[:-1]:
            numstr += numrow[i]
        if len(numstr.strip()) == 0:
            # Next problem
            problem_nums = []
        # Add the number
        else:
            problem_nums.append(int(numstr))
        # If we have an operator, then finalize it
        if grid[-1][i] == "*" or grid[-1][i] == "+":
            total += perform_operation(grid[-1][i], problem_nums)
            problem_nums = [] 
    
    return total


print("part 1 " + str(run_part_1()))
print("part 2 " + str(run_part_2()))