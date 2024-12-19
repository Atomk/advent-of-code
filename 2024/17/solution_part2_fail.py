"""
2024-12-19
A quine finder, interesting! I am amazed that I know this word.
This is dark magic to me, without digging into this it feels
like whoever designed this is pretty smart. Even though
the solution looks easy, I clocked 50 seconds to read the instructions
for this second part and creating a copy of my previous solution.
Let's see if I can solve this as fast as I expect.
"""

from dataclasses import dataclass

@dataclass
class Registers:
    A: int
    B: int
    C: int

def combo_operand_value(operand: int, reg: Registers) -> int:
    if operand <= 3:
        return operand
    match operand:
        case 4: return reg.A
        case 5: return reg.B
        case 6: return reg.C
        case _: raise Exception("This cannot appear in a valid program")

def run(program: list[int], regs: Registers, output: list[int], quine_check: bool = False):
    ip = 0
    append_index = 0
    while ip < len(program):
        opcode = program[ip]
        operand = program[ip+1]
        match opcode:
            case 0:
                value = combo_operand_value(operand, regs)
                regs.A = regs.A // pow(2, value)
            case 1: regs.B = regs.B ^ operand
            case 2: regs.B = combo_operand_value(operand, regs) % 8
            case 3:
                if regs.A != 0:
                    ip = operand
                    continue
            case 4: regs.B = regs.B ^ regs.C
            case 5:
                value = combo_operand_value(operand, regs) % 8
                output.append(value)
                if quine_check:
                    if value != program[append_index]:
                        return False
                    # May be needed instead of the condition above with huge A register values
                    # if append_index >= len(program) or value != program[append_index]:
                    #     break
                    append_index += 1
            case 6:
                value = combo_operand_value(operand, regs)
                regs.B = regs.A // pow(2, value)
            case 7:
                value = combo_operand_value(operand, regs)
                regs.C = regs.A // pow(2, value)
            case _: raise Exception("Unexpected opcode: " + str(opcode))
        ip += 2

    return append_index == len(program)

def run_quine(program: list[int], regs: Registers):
    ip = 0
    append_index = 0
    while ip < len(program):
        opcode = program[ip]
        operand = program[ip+1]
        match opcode:
            case 0:
                value = combo_operand_value(operand, regs)
                # `1 << value` is the same as `pow(2, value)`
                regs.A = regs.A // (1 << value)
            case 1: regs.B ^= operand
            case 2: regs.B = combo_operand_value(operand, regs) % 8
            case 3:
                if regs.A != 0:
                    ip = operand
                    continue
            case 4: regs.B ^= regs.C
            case 5:
                value = combo_operand_value(operand, regs) % 8
                # output.append(value)
                if value != program[append_index]:
                    return False
                # May be needed instead of the condition above with huge A register values
                # if append_index >= len(program) or value != program[append_index]:
                #     break
                append_index += 1
            case 6:
                value = combo_operand_value(operand, regs)
                regs.B = regs.A // (1 << value)
            case 7:
                value = combo_operand_value(operand, regs)
                regs.C = regs.A // (1 << value)
            case _: raise Exception("Unexpected opcode: " + str(opcode))
        ip += 2

    # Prevents false positives if the output is shorter than the program
    return append_index == len(program)

def parse_input(file_path):
    a = 0
    b = 0
    c = 0
    file = open(file_path)
    line_index = 1
    program_int_list: list[int] = []
    while True:
        line = file.readline().strip()
        match line_index:
            case 1: a = int(line[12:])
            case 2: b = int(line[12:])
            case 3: c = int(line[12:])
            case 4: pass
            case 5:
                program_str_list = line[9:].split(",")
                program_int_list.extend([int(n) for n in program_str_list])
            case _: break
        line_index += 1
    file.close()

    return a, b, c, program_int_list

def to_str_list(numbers: list[int]):
    return [str(n) for n in numbers]

def test():
    regs = Registers(0, 0, 0)
    output = []

    # If register C contains 9, the program 2,6 would set register B to 1.
    output.clear()
    regs.C = 9
    run([2,6], regs, output)
    assert(regs.B == 1)

    # If register A contains 10, the program 5,0,5,1,5,4 would output 0,1,2.
    output.clear()
    regs.A = 10
    run([5,0,5,1,5,4], regs, output)
    assert(output == [0,1,2])

    # If register A contains 2024, the program 0,1,5,4,3,0 would output 4,2,5,6,7,7,7,7,3,1,0 and leave 0 in register A.
    output.clear()
    regs.A = 2024
    run([0,1,5,4,3,0], regs, output)
    assert(output == [4,2,5,6,7,7,7,7,3,1,0])
    assert(regs.A == 0)

    # If register B contains 29, the program 1,7 would set register B to 26.
    output.clear()
    regs.B = 29
    run([1,7], regs, output)
    assert(regs.B == 26)

    # If register B contains 2024 and register C contains 43690, the program 4,0 would set register B to 44354.
    output.clear()
    regs.B = 2024
    regs.C = 43690
    run([4,0], regs, output)
    assert(regs.B == 44354)

    # Part 1 sample input test
    output.clear()
    regs.A = 729
    regs.B = 0
    regs.C = 0
    run([0,1,5,4,3,0], regs, output)
    assert(output == [4,6,3,5,6,3,5,2,1,0])

def solution(data_file_path) -> int:
    REG_A_DEFAULT, REG_B_DEFAULT, REG_C_DEFAULT, program = parse_input(data_file_path)

    regs = Registers(0, 0, 0)

    initial_value_A = -1
    #initial_value_A = 710_000_000
    output = []
    while True:
        initial_value_A += 1
        regs.A = initial_value_A
        regs.B = REG_B_DEFAULT
        regs.C = REG_C_DEFAULT
        # output.clear()

        if run_quine(program, regs):
            return initial_value_A
        # if initial_value_A % 10_000_000 == 0:
        #     print(initial_value_A)
        #     # print(program, output, initial_value_A)

    return initial_value_A

"""
...of course not. I'm at 10 minutes and I already made two mistakes,
I was comparing the output string of the previous part (that has commas)
with the output, that I turned into a string but without commas...
After fixing those I see that the comparison is too slow, so I'll avoid
converting the output to a string.
---
25 minutes in, with some print debugging I realized another mistake,
I was not resetting the registers B and C to their default values
at each iteration. Something is still wrong though, I suspect it's
the loop instruction or another oversight on my part.
---
One hour in, sigh. Uncapable of pinpointing the error, I refactored
the implementation and added all tests from the puzzle description.
This took some time, and of course all tests pass, so the implementation
of the instructions is probably correct.
One goal of the refactoring was to separate concerns and put some variables
in different scopes (the fact there is no block scope kinda sucks),
so it's easier to see what could be wrong.
---
I. Feel. So. Stupid.
I did not realize that the sample input for the second part is different
from the sample input for the first part, so I was testing the expected
result against the wring data set. *sign*
Now I get the first test passing, while the second takes a while, as usual,
so I have to optimize a bit. For now I'll abort execution if the values
added to the output are different from what is in the program
text at the same position.
---
That seemed to speed up everything quite a bit. Converting both program
and output to use a list of integers instead of strings also resulted
in a speedup, probably because of skipped conversions.
(getting answer from sample input went from 0.17 sec to 0.135 sec)
Removing the "is_literal" parameter from operand_value() seemed to shave
an additional 0.1-0.2 seconds, interesting.
---
Another good optimization, make run() return whether the output is a quine
or not, so the main function does not have to do equality check.
We are now at 0.123 seconds.
---
Replaced pow(2, value) with 1 << value, another trick discovered
recently during my Ancient Empires decompilation project.
We are now a bit below 0.11 seconds, which is again the time
to get the correct answer for the sample input. I feel like I need
a 10x improvement though to break this wall.
---
Removed "output.append(value)" in run() because it's not needed to check if
the result is a quine, we are now at 0.095 seconds (so -0.1 seconds
compared to previous step)
---
0.092 by creating a run() variant without "is_quine" and "output" parameters.
---
I lost the clock but it's over two hours, I give up. I have no more ideas
and at 710_000_000 iterations still no quine in sight. I don't think
this requires multithreading, I probably missed something else.
That's enough programming for today.
"""

test()

import time
perf_start = time.perf_counter()

# 0.17 seconds // abort run early if output does not match
# 0.135 sec // use ints instead of strings for program and output items
answer_sample = solution("./sample_input_2.txt")

perf_result = time.perf_counter() - perf_start
print(f"Time: {perf_result:.5f} sec")

print("Answer (sample):", answer_sample)
assert(answer_sample == 117440)

answer = solution("./input.txt")
print("Answer:", answer)
# assert(answer == "7,4,2,5,1,4,6,0,4")
