from collections import defaultdict

input_path = "day7.txt"

output_path = "day7_output.txt"

def read_input():
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

def write_grid(grid):
    with open(output_path, 'w') as f:
        for row in grid:
            f.write("".join(row) + "\n")

# This is dumb, but maybe fun to visualize and at least intuitive
def step_part_1(grid):
    updates = 0
    for ridx, row in enumerate(grid[:-1]):
        for cidx, char in enumerate(row):
            if char == "S" and grid[ridx+1][cidx] != "|":
                grid[ridx+1][cidx] = "|"
                updates += 1
            elif char == "|" and grid[ridx+1][cidx] == "^" and (grid[ridx+1][cidx-1] != "|" or grid[ridx+1][cidx+1] != "|"):
                grid[ridx+1][cidx-1] = "|"
                grid[ridx+1][cidx+1] = "|"
                updates += 1
            elif char == "|" and grid[ridx+1][cidx] != "|" and grid[ridx+1][cidx] != "^":
                grid[ridx+1][cidx] = "|"
                updates += 1
    return updates, grid

def score_part_1(grid):
    splits = 0
    for ridx, row in enumerate(grid):
        for cidx, char in enumerate(row):
            if char == "^" and grid[ridx-1][cidx] == "|":
                splits += 1
    return splits

def run_part_1():
    updates = -1
    grid = read_input()
    while updates != 0:
        updates, grid = step_part_1(grid)
    write_grid(grid)
    return score_part_1(grid)

class Node: 
    left = None
    right = None
    col = None
    
    def __init__(self, col):
        self.left = None
        self.right = None
        self.col = col

    def set_left(self, left):
        self.left = left

    def set_right(self, right):
        self.right = right

    def get_children(self):
        return [self.left, self.right]
    
    def get_leaves(self):
        if self.left == None and self.right == None:
            return [self]
        elif self.left != None and self.right != None:
            return self.left.get_leaves() + self.right.get_leaves()
        elif self.left != None:
            return self.left.get_leaves()
        else:
            return self.right.get_leaves()
        
def run_part_2_graph():
    grid = read_input()
    startcol = "".join(grid[0]).find("S")
    root = Node(startcol)
    col_to_node_map = defaultdict(lambda: [])
    col_to_node_map[startcol].append(root)
    for ridx, row in enumerate(grid[:-1]):
        created_nodes = 0
        for cidx, char in enumerate(row):
            if char == "^":
                nodes = col_to_node_map[cidx].copy()
                # For each leaf node at the current column, create two new leaves off of it
                for node in nodes:
                    left = Node(cidx-1)
                    right = Node(cidx+1)
                    node.set_left(left)
                    node.set_right(right)
                    col_to_node_map[cidx].remove(node)
                    col_to_node_map[cidx-1].append(left)
                    col_to_node_map[cidx+1].append(right)
                    created_nodes += 2
        print(f"Created {str(created_nodes)} nodes for row {str(ridx)} [{str(row)}]")
    return len(root.get_leaves())


def run_part_2_counting():
    grid = read_input()
    path_counts = defaultdict(lambda: 0)
    startcol = "".join(grid[0]).find("S")
    path_counts[startcol] = 1
    for ridx, row in enumerate(grid[:-1]):
        for cidx, char in enumerate(row):
            if char == "^":
                path_counts[cidx-1] += path_counts[cidx]
                path_counts[cidx+1] += path_counts[cidx]
                path_counts[cidx] = 0
    total = 0
    for i in range(len(grid[0])):
        total += path_counts[i]
    return total

print(f"Part 1 : {run_part_1()}")
print(f"Part 2 : {run_part_2_counting()}")
# print(f"Part 2 : {run_part_2_graph()}")