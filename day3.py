input_path = "day3.txt"

def read_input():
    with open(input_path) as f:
        for line in f:
            yield str(line)

def get_max_joltage_for_bank(bank):
 # The largest possible number with 2 digits will just greedily select the largest digit for each
    for i in range(9, -1, -1):
        i_idx = bank.find(str(i))
        # If we're in any valid posn, then use this tens digit 
        if i_idx >= 0 and i_idx < len(bank) - 2:
            # Do the same for the next digit
            for j in range(9, -1, -1):
                j_idx = bank[i_idx+1:].find(str(j))
                # If we're in any valid posn, then use this ones digit 
                if j_idx >= 0:
                        return int(str(i) + str(j))
                
def get_max_joltage_in_substr(substr, remaining_digits, joltage, og_bank):
    print("ITR: REMAINING DIGITS: " + str(remaining_digits))
    if remaining_digits <= 0:
        print("RETURNING " + joltage + " FROM " + og_bank)
        return int(joltage)
    # Early exit when we're out of options
    if len(substr) == remaining_digits:
        print("RETURNING " + joltage + substr + " FROM " + og_bank)
        return int(joltage + substr)
    searchable_substr = substr[:len(substr)-(remaining_digits-1)]
    print("SEARCHABLE SUBSTR : " + searchable_substr)
    for i in range(9,-1,-1):
        i_idx = searchable_substr.find(str(i))
        if i_idx >= 0:
            print("Selecting " + str(i) + " from " + substr + " and passing on " + substr[i_idx+1:])
            return get_max_joltage_in_substr(substr[i_idx+1:], remaining_digits - 1, joltage + str(i), og_bank)
    print("FAILED TO FIND MATCH FOR " + str(substr) + " with " + str(remaining_digits) + " REMAINING DIGITS AND JOLTAGE " + str(joltage) + " FROM BANK " + str(og_bank))

def run_part_1():

    joltage_sum = 0

    for bank in read_input():
       joltage_sum += get_max_joltage_for_bank(bank)               

    return joltage_sum


def run_part_2():

    joltage_sum = 0

    for bank in read_input():
       print("=== DEBUG: BANK ===")
       joltage_sum += get_max_joltage_in_substr(bank.strip(), 12, "", bank.strip())               

    return joltage_sum

def test_part_2():

    test_inputs = [str(987654321111111), str(811111111111119), str(234234234234278), str(818181911112111), str(1000000099990000000)]
    broken_test_input = [str(443242123312333253332142242332364333242132343344434449423442131631252423312726246312333222)]

    for test in broken_test_input:
       print(test + " : " + str(get_max_joltage_in_substr(test, 12, "", test)))

# test_part_2()

print("Part 1 Result " + str(run_part_1()))
print("Part 2 Result " + str(run_part_2()))