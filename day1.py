input_path = "day1.txt"

def read_input():
    with open(input_path) as f:
        for line in f:
            yield line[0] == "R", int(line[1:])

def run_part_1():
    pos = 50
    password = 0

    def update_posn(current_posn, is_right, num):
        nonlocal password
        delta = num % 100
        if is_right:
            current_posn += delta
            if current_posn > 99:
                current_posn -= 100
        else:
            current_posn -= delta
            if current_posn < 0:
                current_posn += 100
        return current_posn

    for is_right, num in read_input():
        pos = update_posn(pos, is_right, num)
        if pos == 0:
            password += 1
    return str(password)

def run_part_2():
    pos = 50
    password = 0

    def update_posn(current_posn, is_right, num):
        nonlocal password
        delta = num % 100
        password += num // 100
        if is_right:
            current_posn += delta
            if current_posn > 99:
                current_posn -= 100
                password += 1
        else:
            started_at_0 = current_posn == 0
            current_posn -= delta
            if current_posn < 0:
                current_posn += 100
                if not started_at_0:
                    password += 1
            elif current_posn == 0:
                password += 1
        return current_posn

    for is_right, num in read_input():
        pos = update_posn(pos, is_right, num)
    return str(password)

print("Part 1:", run_part_1())
print("Part 2:", run_part_2())

