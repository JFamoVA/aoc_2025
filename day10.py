import copy
import re

input_path = "day10.txt"

def read_input():
    with open(input_path) as f:
        problems = []
        for row in f:
            rowd = dict()
            # Find target
            target_matches = re.findall(r'\[(.*?)\]', row)
            target_str = target_matches[0]
            target_str = target_str.replace("[", "")
            target_str = target_str.replace("]", "")
            target_str = target_str.replace("#", "1")
            target_str = target_str.replace(".", "0")
            rowd["target"] = target_str
            # Find buttons
            button_matches = re.findall(r'\(\d+(?:,\d+)*\)', row)
            rowd["buttons"] = []
            for bm in button_matches:
                bm = bm.replace("(","")
                bm = bm.replace(")","")
                bis = bm.split(",")
                rowd["buttons"].append([int(bi) for bi in bis])
            # Find joltage
            jlts_m = re.findall(r'\{\d+(?:,\d+)*\}', row)
            jlt = jlts_m[0]
            jlt = jlt.replace("{","")
            jlt = jlt.replace("}","")
            jlts = jlt.split(",")
            rowd["joltage"] = [int(j) for j in jlts]
            # Add
            problems.append(rowd)
        return problems

    
def print_input(problems):
    for prob in problems:
        print("===")
        print(f"Target: {prob['target']}")
        print(f"Buttons: {prob['buttons']}")
        print(f"Joltage: {prob['joltage']}")

def apply_state_change(state, button):
    ns = state
    for b in button:
        old = ns[b]
        newc = "1" if old == "0" else "0"
        ns = ns[:b] + newc + ns[b+1:]
    return ns

def solve_problem(problem):
    target = problem["target"]
    targetlen = len(target)
    initialstate = "".join(["0" for i in range(targetlen)])

    if initialstate == target:
        return 0

    solved_states = dict()
    solved_states[initialstate] = 0

    state_stack = [(initialstate, 0)]

    itrs = 0
    itr_limit = 1000

    while len(state_stack) > 0:
        itrs += 1
        if itrs > itr_limit:
            print("Breaking from iterations with stack " + str(state_stack) + " and solved " + str(solved_states))
            return 0
        
        state_and_num = state_stack.pop(0)
        state = state_and_num[0]
        num = state_and_num[1]
        for button in problem["buttons"]:
            # Apply this state change
            new_state = apply_state_change(state, button)
            if new_state == target:
                return num + 1
            elif new_state in solved_states:
                continue
            else:
                solved_states[new_state] = num + 1
                state_stack.append((new_state, num + 1))

def solve_joltage_problem(problem):
    target = problem["joltage"]
    targetlen = len(target)
    initialstate = [0 for i in range(targetlen)]

    # TODO format to be valid index

    if initialstate == target:
        return 0

    solved_states = dict()
    solved_states[initialstate] = 0

    state_stack = [(initialstate, 0)]

    itrs = 0
    itr_limit = 1000

    while len(state_stack) > 0:
        itrs += 1
        if itrs > itr_limit:
            print("Breaking from iterations with stack " + str(state_stack) + " and solved " + str(solved_states))
            return 0
        
        state_and_num = state_stack.pop(0)
        state = state_and_num[0]
        num = state_and_num[1]
        for button in problem["buttons"]:
            # Apply this state change
            new_state = apply_state_change(state, button)
            if new_state == target:
                return num + 1
            elif new_state in solved_states:
                continue
            else:
                solved_states[new_state] = num + 1
                state_stack.append((new_state, num + 1))


def run_part_1():
    probs = read_input()
    # print_input(probs)
    sumj = 0
    for prob in probs:
        sumj += solve_problem(prob)
    return sumj

def run_part_2():
    probs = read_input()
    print_input(probs)
    # sumj = 0
    # for prob in probs:
    #     sumj += solve_problem(prob)
    # return sumj

# print(f"Part 1 : {run_part_1()}")
print(f"Part 2 : {run_part_2()}")