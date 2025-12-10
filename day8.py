import math
import collections

input_path = "day8.txt"
sample_input_path = "day8_sample.txt"

class Box:
    def __init__(self,id,x,y,z):
        self.id = id
        self.x = x
        self.y = y
        self.z = z
        self.distances = dict()
        self.connections = set({id})
        self.direct_connections = set()

    def set_distance(self, other_id, distance):
        self.distances[other_id] = distance

    def get_distance(self, other_id):
        if other_id in self.distances:
            return self.distances[other_id]
        else:
            return None
        
    def sort_distances(self):
        self.distances = dict(sorted(self.distances.items(), key=lambda item: item[1]))
        
    def print_distances(self):
        return ",".join([str(int(dist)) for dist in list(self.distances.values())])

    def connect(self, other_id, boxmap):
        if other_id == self.id:
            raise "Trying to connect to ourselves"
        self.direct_connections.add(other_id)
        self.connections.add(other_id)
        # Make sure to grab their connections first
        self.connections = self.connections.union(boxmap[other_id].get_connections())
        # Inner-connect each other one of my connections to this new id
        for conn in self.connections:
            boxmap[conn].union_connect(self)
            self.union_connect(boxmap[conn])

    def union_connect(self, other_box):
        self.connections = self.connections.union(other_box.get_connections())

    def direct_connect(self, other_id):
        # self.connections.add(other_id)
        if other_id != self.id:
            self.direct_connections.add(other_id)

    def get_connections(self):
        return self.connections
    
    def get_closest_unconnected(self):
        for key in self.distances:
            if not key in self.direct_connections:
                return key, self.distances[key]

def read_input(filepath=input_path):
    boxmap = dict()
    with open(filepath) as f:
        for ridx, row in enumerate(f):
            coords = row.split(",")
            coords = [int(c) for c in coords]
            boxmap[ridx] = Box(ridx, coords[0], coords[1], coords[2])
    return boxmap

def calc_distance(box1, box2):
    return math.sqrt(math.pow(box1.x - box2.x, 2) + math.pow(box1.y - box2.y,2) + math.pow(box1.z - box2.z, 2))

def compute_distances(boxes):
    for i in range(len(boxes)):
        for j in range(len(boxes)):
            box = boxes[i]
            other_box = boxes[j]
            if box != other_box:
                # print(f"Skipping because {box.id} = {other_box.id}")
                if box.get_distance(other_box.id) == None:
                    d = calc_distance(box, other_box)
                    box.set_distance(other_box.id, d)
                    other_box.set_distance(box.id, d)
                    # print(f"Calculated distance between {box.id} and {other_box.id} as {d}")
        box.sort_distances()
        # print(f"DEBUG: Box {box.id} distances {str(box.print_distances())}")

    return boxes

def run_compute_distances():
    boxes = read_input()
    boxes_list = list(boxes.values())
    compute_distances(boxes_list)
    print("== Done finding distances ==")

def find_min_unconnected_distance(boxes):
    min_dist = math.inf
    min_box_1 = None
    min_box_2_id = None
    for box in boxes:
        other_id, dist = box.get_closest_unconnected()

        # print(f"Box {box.id} has closest unconn {dist}")

        if dist < min_dist:
            min_dist = dist
            min_box_1 = box
            min_box_2_id = other_id

    return min_dist, min_box_1, min_box_2_id

def connect_closest_unconnected_boxes(id_to_box_map, debug=False):
    min_dist, min_box_1, min_box_2_id = find_min_unconnected_distance(id_to_box_map.values())
    min_box_1.connect(min_box_2_id, id_to_box_map)
    id_to_box_map[min_box_2_id].direct_connect(min_box_1.id)
    if debug:
        print(f"=== Connected Boxes {str(min_box_1.id)} and {min_box_2_id} with distance {min_dist}")
        print(f"Product of X coords is {min_box_1.x * id_to_box_map[min_box_2_id].x}")

def connect_all_except(id_to_box_map, skip_ids):
    base_box = id_to_box_map[0]
    for i in range(1,1000):
        if i not in skip_ids:
            base_box.connect(i, id_to_box_map)
            id_to_box_map[i].direct_connect(base_box.id)

def get_circuit_sizes(boxes):
    id_to_csize = dict()
    for box in boxes:
        if not box_conns_in_map(id_to_csize, box):
            id_to_csize[box.id] = len(box.get_connections())
    return sorted(id_to_csize.items(), key=lambda x: x[1])

def box_conns_in_map(map, box):
    for conn in box.get_connections():
        if conn in map.keys():
            return True
    return False

def run_part_1():
    boxmap = read_input()
    compute_distances(list(boxmap.values()))
    print("===Computed Distances===")
    for i in range(1000):
        connect_closest_unconnected_boxes(boxmap)
    csizes = get_circuit_sizes(boxmap.values())

    print(f"Got largest circuit sizes " + str(csizes))
    print(f"Product of 3 largest " + str(csizes[-1][1] * csizes[-2][1] * csizes[-3][1]))

def run_test():
    boxmap = read_input(sample_input_path)
    compute_distances(list(boxmap.values()))
    print("===Computed Distances===")
    for i in range(10):
        connect_closest_unconnected_boxes(boxmap)
    csizes = get_circuit_sizes(boxmap.values())

    print(f"Got largest circuit sizes " + str(csizes))
    print(f"Product of 3 largest " + str(csizes[-1][1] * csizes[-2][1] * csizes[-3][1]))

# run_test()
# run_part_1()

def run_part_2():
    boxmap = read_input()
    compute_distances(list(boxmap.values()))
    print("===Computed Distances===")

    # We know these are the last 3 to be connected
    connect_all_except(boxmap, {734, 876, 920})
    csizes = get_circuit_sizes(boxmap.values())

    while len(csizes) > 1:
        connect_closest_unconnected_boxes(boxmap, debug=True)
        csizes = get_circuit_sizes(boxmap.values())

    print(f"Got largest circuit sizes " + str(csizes))
    print(f"Product of 3 largest " + str(csizes[-1][1] * csizes[-2][1] * csizes[-3][1]))

run_part_2()