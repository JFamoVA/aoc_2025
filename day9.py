import math


input_path = "day9.txt"
output_path = "day9_output.txt"

def read_input():
    coords = []
    with open(input_path) as f:
        for row in f:
            c = row.strip().split(",")
            coords.append((int(c[0]), int(c[1])))
    return coords

def write_grid(grid):
    with open(output_path, 'w') as f:
        for row in grid:
            f.write("".join(row))

def write_xs_and_os():
    coords = read_input()
    grid = [["." for i in range(100000)] for j in range(100000)]
    last_coord = coords[-1]
    ctr = 0
    for red in coords:
        print(f"=== Writing {ctr}/{len(coords)}")
        grid[red[0]][red[1]] = "#"
        if red[0] > last_coord[0]:
            for x in range(last_coord[0]+1, red[1]):
                grid[x][red[1]] = "X"
        elif red[0] < last_coord[0]:
            for x in range(red[0]+1, last_coord[0]):
                grid[x][red[1]] = "X"
        elif red[1] > last_coord[1]:
            for y in range(last_coord[1]+1, red[1]):
                grid[red[0]][y] = "X"
        else:
            for y in range(red[1]+1, last_coord[1]):
                grid[red[0]][y] = "X"
        ctr += 1
    write_grid(grid)


def brute_force_part_1():
    coords = read_input()
    max_area = 0
    for c1 in coords:
        for c2 in coords: 
            area = abs(c1[0]-c2[0]+1) * abs(c1[1]-c2[1]+1)
            if area > max_area:
                max_area = area
    return max_area

def is_point_in_shape_horizontally(point, hor_segments):
    inside = False
    for h in hor_segments:
        if h[0] <= point[0] and h[1] >= point[0]:
            if point[1] == h[2]:
                return True
            if point[1] < h[2]:
                return inside
            if (point[0] == h[0] or point[0] == h[1]):
                inside = True # We can never flip inside-ness on a boundary
            else:
                inside = not inside
    return inside

def is_point_in_shape_vertically(point, vert_segments):
    inside = False
    for v in vert_segments:
        # print(f"Considering vertical segment {str(v)}...")
        if v[0] <= point[1] and v[1] >= point[1]:
            if point[0] == v[2]:
                return True
            if point[0] < v[2]:
                return inside
            if (point[1] == v[0] or point[1] == v[1]):
                inside = True # We can never flip inside-ness on a boundary
            else:
                inside = not inside
            # print(f"Flipping inside...")
    return inside
    
def is_point_in_shape(point, hor_segments, vert_segments):
    return is_point_in_shape_horizontally(point, hor_segments) and is_point_in_shape_vertically(point, vert_segments)

def is_shape_valid(minx, maxx, miny, maxy, hs, vs):
    # Has no line segments inside of it
    for h in hs:
        if ((h[0] > minx and h[0] < maxx) or (h[1] > minx and h[1] < maxx)) and (h[2] > miny and h[2] < maxy):
            # print(f"Failing shape because hseg {str(h)} is inside of shape {minx},{maxx} x {miny},{maxy}")

            is_sandwiched = False

            # Edge case: this shouldn't fail if there's another hseg directly above or below me
            for oh in hs:
                if oh[2] == h[2]+1 or oh[2] == h[2]-1:
                    is_sandwiched = True
            
            if not is_sandwiched:
                return False
    for v in vs:
        if ((v[0] > miny and v[0] < maxy) or (v[1] > miny and v[1] < maxy)) and (v[2] > minx and v[2] < maxx):
            # print(f"Failing shape because vseg {str(v)} is inside of shape {minx},{maxx} x {miny},{maxy}")

            is_sandwiched = False

            # Edge case: this shouldn't fail if there's another vsed directly beside me
            for ov in vs:
                if ov[2] == v[2]+1 or ov[2] == v[2]-1:
                    is_sandwiched = True

            if not is_sandwiched:
                return False
    return True

def draft_part_2(coords):
    vert_segments = []
    hor_segments = []
    last_coord = coords[-1]
    
    # Build a set of horizontal and vertical segments
    for coord in coords:
        if coord[0] > last_coord[0] or coord[0] < last_coord[0]:
            minc = min(coord[0], last_coord[0])
            maxc = max(coord[0], last_coord[0])
            hor_segments.append((minc, maxc, coord[1]))
        else:
            minc = min(coord[1], last_coord[1])
            maxc = max(coord[1], last_coord[1])
            vert_segments.append((minc, maxc, coord[0]))
        last_coord = coord

    # Sort in order of appearance
    hor_segments = sorted(hor_segments, key=lambda seg: seg[2])
    vert_segments = sorted(vert_segments, key=lambda seg: seg[2])

    # print("==DEBUG got horizontal segments: " + str(hor_segments))
    # print("==DEBUG got vertical segments: " + str(vert_segments))

    # Check if each point is in the shape
    max_area = 0
    for c1 in coords:
        for c2 in coords: 
            if is_shape_valid(min(c1[0],c2[0]), max(c1[0],c2[0]), min(c1[1],c2[1]), max(c1[1],c2[1]), hor_segments, vert_segments):
                area = (abs(c1[0]-c2[0])+1) * (abs(c1[1]-c2[1])+1)
                if area > max_area:
                    max_area = area
                    print(f"Found max area between {str(c1)} and {str(c2)}")
            # if is_point_in_shape((c1[0],c2[1]), hor_segments, vert_segments) and is_point_in_shape((c2[0],c1[1]), hor_segments, vert_segments):
                
                # else:
                    # print(f"Shape is invalid between {str(c1)} and {str(c2)}")
            # else: 
                # print(f"Point is invalid for {str(c1)} and {str(c2)}")
                # print(f"{str((c1[0],c2[1]))} in shape? {is_point_in_shape((c1[0],c2[1]), hor_segments, vert_segments)}")
                # print(f"{str((c2[0],c1[1]))} in shape? {is_point_in_shape((c2[0],c1[1]), hor_segments, vert_segments)}")
    
    # DEBUG
    # print(f"9,3 in hor {is_point_in_shape_horizontally((9,3), hor_segments)}")
    # print(f"9,3 in vert {is_point_in_shape_vertically((9,3), vert_segments)}")

    return max_area

def test_part_2():
    test_coords = [(7,1),(11,1),(11,7),(9,7),(9,5),(2,5),(2,3),(7,3)]
    print(f"Tested Part 2: {draft_part_2(test_coords)}")


def has_off_by_1_coords(coords):
    for coord in coords:
        for other in coords:
            if abs(coord[0] - other[0]) == 1 or abs(coord[1] - other[1]) == 1:
                return True
    return False


# print(f"Part 1 : {brute_force_part_1()}")
# write_xs_and_os()
# test_part_2()
print(f"Has off by 1 coords {str(has_off_by_1_coords(read_input()))}")
print(f"Part 2 : {draft_part_2(read_input())}")