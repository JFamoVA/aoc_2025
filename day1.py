input_path = "day1.txt"

def run_part_1():

    pos = 50
    password = 0

    def update_posn(current_posn, is_right, num):
        # nonlocal is for outer function definition, global would be for module definition
        nonlocal password
        delta = num % 100
        if(is_right):
            current_posn += delta
            if(current_posn > 99):
                current_posn = current_posn - 100
        else:
            current_posn -= delta
            if(current_posn < 0):
                current_posn = current_posn + 100

        return current_posn

    with open(input_path, 'r') as input_file:
        for line in input_file:
            is_right = line[0] == "R"
            num = int(line[1:])

            pos = update_posn(current_posn=pos, is_right=is_right, num=num)

            if(pos == 0):
                password += 1
    return str(password)

def run_part_2():

    pos = 50
    password = 0

    def update_posn(current_posn, is_right, num):
        nonlocal password
        delta = num % 100
        # Include full 100 rotations
        # Recall, int() is fine here vs floor() bcs we only need to truncate. Never deal with negative num
        full_passes = int(num / 100)
        password += full_passes
        if(is_right):
            current_posn += delta
            if(current_posn > 99):
                current_posn = current_posn - 100
                password += 1
        else:
            started_at_0 = current_posn == 0
            current_posn -= delta
            if(current_posn < 0):
                current_posn = current_posn + 100
                if not started_at_0:
                    password += 1
            elif(current_posn == 0):
                password += 1

        return current_posn

    with open(input_path, 'r') as input_file:
        for line in input_file:
            is_right = line[0] == "R"
            num = int(line[1:])

            pos = update_posn(current_posn=pos, is_right=is_right, num=num)
    return str(password)
        
print("Part 1 " + run_part_1())

print("Part 2 " + run_part_2())

