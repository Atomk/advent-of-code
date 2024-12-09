from collections import namedtuple
Equation = namedtuple("Equation", ["result", "operands"])

"""
Take two. No point in keeping track of the time here,
I just want to fix my previous attempt and know what to do.
"""

"""
Yesterday after discovering my implementation mistake in the
previous attempt I just couldn't stop thinking about this damn combinations generator.
Before turning off the computer I tried to see if I could
adapt my previous solution to use base 3 instead of base 2 (binary),
but I soon realized there's no easy way to do it and did not like that path.
So in the end I had to think through the problem of generating combinations,
and it turned out to be much easier than it seemed.
In fact the implementation I had in mind is so straightforward
I wrote this function on my phone before going to bed, didn't even need recursion.
The only downside it that it takes some memory to generate a new
list for every combination, an iterator (for each call return a sequence,
or mutate the sequence) with some adjustments would be better.
"""
def generate_combinations(base, length) -> list[list[int]]:
    combinations = []
    sequence = [0] * length
    combinations.append(sequence.copy())
    pos = 0
    while True:
        sequence[pos] += 1
        while sequence[pos] >= base:
            if pos + 1 >= length:
                return combinations
            sequence[pos] = 0
            pos += 1
            sequence[pos] += 1
        pos = 0
        combinations.append(sequence.copy())

def can_be_correct(expected_result, numbers):
    operators_count = len(numbers) - 1
    op_combinations = generate_combinations(3, operators_count)
    for combination in op_combinations:
        result = numbers[0]
        # skip first operand since it's already loaded in the result variable
        num_index = 1
        for op in combination:
            if op == 0:
                result += numbers[num_index]
            if op == 1:
                result *= numbers[num_index]
            if op == 2:
                merged_strings = str(result) + str(numbers[num_index])
                result = int(merged_strings)
            num_index += 1
        if result == expected_result:
            return True

    return False

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
        if can_be_correct(eq.result, eq.operands):
            correct_equations_sum += eq.result

    return correct_equations_sum

"""
Got it right finally! Took two tries because I forgot a "break"
inside the main equations loop, a copy-paste blunder,
so the code was processing just the first equation in the file.
I really like the the code is much simpler than my previous attempt,
I also avoided copying the numbers list to merge the values
which is a nice improvement.
Calculations for the puzzle input take quite a bit, I did not measure
it yet but it feels like 10 seconds at least.
I could improve performance by not generating a different list for every
combination (that iterator idea sounds promising), or using tuples.
I might try it and see how mny seconds can be shaved,
if it wasn't python I'd play with data types and use arrays instead of lists
"""

print("Answer part 2 (sample):", part2("./sample_input.txt"))
assert(part2("./sample_input.txt") == 11387)
print("Answer part 2:", part2("./input.txt"))
assert(part2("./input.txt") == 149956401519484)
