from collections import namedtuple
Equation = namedtuple("Equation", ["result", "operands"])

def is_bit_on(value, bit_index):
    return (1 << bit_index) & value != 0

def part1(data_file_path) -> int:
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
        operators_count = len(eq.operands) - 1
        combinations_count = pow(2, operators_count)
        # A progressive number which will be read as a sequence of bits
        # (0 and 1 which will translate to addition or multiplication)
        for combination_of_operators in range(combinations_count):
            test_result = eq.operands[0]
            for bit_index in range(operators_count):
                if is_bit_on(combination_of_operators, bit_index):
                    # skip first operand since it's already loaded in the result variable
                    test_result += eq.operands[bit_index + 1]
                else:
                    test_result *= eq.operands[bit_index + 1]
            if test_result == eq.result:
                correct_equations_sum += eq.result
                # Break the combinations check loop
                break

    return correct_equations_sum

"""
First try (with proper input), 45 minutes of which at least 15 were dedicated to
refactoring to make the combinations check part easier to read,
I think the way I generated combinations is pretty clever given the puzzle constraints:
each operand can either be addition or multiplication, so like 0 or 1,
which made me thin...a binary number is a sequence of 0 and 1s,
and it's really easy to generate all possible combinations of 0 and 1s
of a specific length (so for a specific number of operands).

Usually "clever" code is frowned upon, but honestly I remember very little about
the math for this kind of things and this is the best I could do with what I know,
I'm sure there are easier, more generic or more readable ways to generate combinations.
Or permutations, which was it?

I run the code four times in total, first two times against the sample input
and the output was wrong because I forgot to reset the "test_result" each iteration
(put the reset before the combinations loop), third time I got the correct result
and fourth time I got the correct result for the proper input file.
Overall I'm pretty satisfied, also because I wasted a lot of time on the day 6 part 2
thing and it was the first time I could not make it work and it was really frustrating.
I haven't had any time to work on this on Saturday so I am also late
and I don't want to fall behind too much.

I guess the second part will be the same thing but taking into account
the operator precedence (will force me to restructure my code),
or the same thing but also with subtraction and division
(which sucks because I cannot use binary sequences)
EDIT: Oh, I was wrong. Really glad it was something less predictable
"""

print("Answer part 1:", part1("./sample_input.txt"))
assert(part1("./sample_input.txt") == 3749)
print("Answer part 1:", part1("./input.txt"))
assert(part1("./input.txt") == 12839601725877)
