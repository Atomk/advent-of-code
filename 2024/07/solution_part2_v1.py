from collections import namedtuple
Equation = namedtuple("Equation", ["result", "operands"])

def is_bit_on(value, bit_index):
    return (1 << bit_index) & value != 0

def can_be_correct(result, operands):
    if len(operands) == 1:
        return result == operands[0]

    operators_count = len(operands) - 1

    combinations_count = pow(2, operators_count)
    # A progressive number which will be read as a sequence of bits
    # (0 and 1 which will translate to addition or multiplication)
    for combination_of_operators in range(combinations_count):
        test_result = operands[0]
        for bit_index in range(operators_count):
            if is_bit_on(combination_of_operators, bit_index):
                # skip first operand since it's already loaded in the result variable
                test_result += operands[bit_index + 1]
            else:
                test_result *= operands[bit_index + 1]
        if test_result == result:
            return True

def get_all_merge_combinations(numbers):
    combinations = []
    operators_count = len(numbers) - 1
    combinations_count = pow(2, operators_count)
    # A progressive number which will be read as a sequence of bits
    # (0 and 1, if 1 then merge operands
    for combination_of_operators in range(combinations_count):
        numbers_copy = numbers.copy()
        bit_index = 0
        number_index = 0
        while number_index + 1 < len(numbers_copy):
            if is_bit_on(combination_of_operators, bit_index):
                removed = numbers_copy.pop(number_index + 1)
                merged_strings = str(numbers_copy[number_index]) + str(removed)
                numbers_copy[number_index] = int(merged_strings)
            else:
                number_index += 1
            bit_index += 1
        # Convert to tuple for hopefully better performance
        # combinations.append((x for x in numbers_copy))
        combinations.append(numbers_copy)

    return combinations

def part2(data_file_path) -> int:
    file = open(data_file_path)
    equations: list[Equation] = []
    for line in file:
        parts = line.split(":")
        operands_strings = parts[1].strip().split()
        result = int(parts[0])
        operands = [int(x) for x in operands_strings]
        equations.append(Equation(result, operands))
    file.close()

    correct_equations_sum = 0
    for eq in equations:
        merge_combinations = get_all_merge_combinations(eq.operands)
        print(eq.result, merge_combinations)
        for operands_list in merge_combinations:
            if can_be_correct(eq.result, operands_list):
                print("ok")
                correct_equations_sum += eq.result
                break

    return correct_equations_sum

"""
1 hour in, after hitting a debugging wall I checked sample input
and explanation for passing equations again, I finally realized my mistake:
"7290: 6 8 6 15 can be made true using 6 * 8 || 6 * 15."
My solution does not account for this case, I cannot make this with two passes. Well, shit!

I knew since I started that overall my solution is very sad and ugly
but I hoped it would work. I guess that's the price I pay to for being
a bit too strict in my implementation for the first part, I guess sometimes
performance reduces extensibility. I can reuse some of what I wrote but
I'll need to rethink how to solve the combinatorics stuff, or do some
very much needed refresh on the topic and retry with better knowledge.
"""

print("Answer part 2 (sample):", part2("./sample_input.txt"))
# assert(part2("./sample_input.txt") == 11387)
# print("Answer part 2:", part2("./input.txt"))
# assert(part2("./input.txt") == ???)
