input_path = "day4.txt"

size = 140

def read_input():
    with open(input_path) as f:
        grid = [["N" for _ in range(size)] for _ in range(size)]
        for row, rowtext in enumerate(f):
            for col,coltext in enumerate(rowtext.strip()):
                grid[row][col] = coltext
        return grid

def count_adjacent_rolls(grid, x, y):
    adjcount = 0
    for dx in range (-1, 2):
        for dy in range(-1, 2):
            if not(dx == 0 and dy == 0) and x+dx >= 0 and y+dy >= 0 and x+dx < size and y+dy < size:
                if grid[x+dx][y+dy] == "@":
                    adjcount += 1
    return adjcount

def run_part_1(grid):
    access_count = 0

    for row, rowtext in enumerate(grid):
        for col,coltext in enumerate(rowtext):
            if coltext == "@":
                if count_adjacent_rolls(grid, row, col) < 4:
                    access_count += 1
    
    return access_count


def run_removal_step(grid):
    access_count = 0
    for row, rowtext in enumerate(grid):
        for col,coltext in enumerate(rowtext):
            if coltext == "@":
                if count_adjacent_rolls(grid, row, col) < 4:
                    access_count += 1
                    grid[row][col] = "R"
    return access_count, grid

def run_part_2():
    new_access_count = -1
    access_count_sum = 0
    grid = read_input()

    while new_access_count != 0:
        new_access_count, grid = run_removal_step(grid)
        access_count_sum += new_access_count
    
    return access_count_sum


print("Part 1 : " + str(run_part_1(read_input())))
print("Part 2 : " + str(run_part_2()))