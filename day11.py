input_path = "day11.txt"

def read_input():
    with open(input_path) as f:
        conns = dict()
        for row in f:
            row = row.strip().replace(":","")
            source = row[:3]
            other = row[4:]
            outputs = other.split(" ")
            conns[source] = outputs
        return conns

def print_conns(conns):
    for item in conns.items():
        print(f"{item[0]} : {item[1]}")

def get_input_dict(conns):
    inputs = dict()
    for node in list(conns.keys()):
        inplist = []
        for item in conns.items():
            if node in item[1]:
                inplist.append(item[0])
        inputs[node] = inplist
    return inputs

computed = dict()

def get_paths_between(input, output, conns):
    if input == output:
        return 1

    pathkey = input + output
    if pathkey in computed:
        return computed[pathkey]
    
    paths = 0
    for out in conns[input]:
        paths += get_paths_between(out, output, conns)

    print(f"Computed {paths} paths between {input} and {output}")

    computed[pathkey] = paths
    return paths

def run_part_1():
    conns = read_input()
    # print("=== OUTPUTS ===")
    # print_conns(conns)
    inputs = get_input_dict(conns)
    # print("=== INPUTS ===")
    # print_conns(inputs)

    answer = get_paths_between("you", "out", conns)
    print(f"Answer : {answer}")

computed_2 = dict()
computed_df = dict()
computed_d = dict()
computed_f = dict()

def get_paths_between_2(input, output, conns, has_d, has_f):
    if input == output:
        if has_d and has_f:
            return 1
        else:
            return 0
        
    refdict = None
    if has_d and has_f:
        refdict = computed_2
    elif has_d and not has_f:
        refdict = computed_d
    elif not has_d and has_f:
        refdict = computed_f
    else:
        refdict = computed_df

    pathkey = input + output
    if pathkey in refdict:
        return refdict[pathkey]
    
    paths = 0
    for out in conns[input]:
        paths += get_paths_between_2(out, output, conns, input == "dac" or has_d, input == "fft" or has_f)

    print(f"Computed {paths} paths between {input} and {output}")

    refdict[pathkey] = paths
    return paths

def run_part_2():
    conns = read_input()
    # print("=== OUTPUTS ===")
    # print_conns(conns)
    # inputs = get_input_dict(conns)
    # print("=== INPUTS ===")
    # print_conns(inputs)

    answer = get_paths_between_2("svr", "out", conns, False, False)
    print(f"Answer : {answer}")


# run_part_1()
run_part_2()