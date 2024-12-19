"""
2024-12-19
I'm doing this today after completing day 19 (two stars!) since now I have time.
I did not look at the puzzle in advance, so no advantage here. Let's go.
---
Woah, we're writing an interpreter! I did that with COW a few years ago,
pretty interesting! I read carefully the first half of the description
then skimmed the rest, since I'll have to look at it anyway for the
implementation of the instructions.
"""

def solution(data_file_path) -> str:
    register_A = 0
    register_B = 0
    register_C = 0
    program: list[str] = []

    file = open(data_file_path)
    line_index = 1
    while True:
        line = file.readline().strip()
        match line_index:
            case 1: register_A = int(line[12:])
            case 2: register_B = int(line[12:])
            case 3: register_C = int(line[12:])
            case 4: pass
            case 5: program.extend(line[9:].split(","))
            case _: break
        line_index += 1
    file.close()

    def operand_value(operand: str, is_literal: bool) -> int:
        value = int(operand)
        if is_literal:
            return value
        else:
            if value <= 3:
                return value
            match operand:
                case "4": return register_A
                case "5": return register_B
                case "6": return register_C
                case _: raise Exception("This cannot appear in a valid program")

    output = []
    ip = 0
    while ip < len(program):
        opcode = program[ip]
        operand = program[ip+1]
        match opcode:
            case "0":
                value = operand_value(operand, False)
                register_A = register_A // pow(2, value)
            case "1":
                register_B = register_B ^ operand_value(operand, True)
            case "2":
                register_B = operand_value(operand, False) % 8
            case "3":
                if register_A != 0:
                    ip = operand_value(operand, True)
                    continue
            case "4":
                register_B = register_B ^ register_C
            case "5":
                value = operand_value(operand, False) % 8
                output.append(str(value))
            case "6":
                value = operand_value(operand, False)
                register_B = register_A // pow(2, value)
            case "7":
                value = operand_value(operand, False)
                register_C = register_A // pow(2, value)
        ip += 2

    return ",".join(output)

"""
Done in 40 minutes first try, it's not hard, you just have to be
really careful with the implementation because debugging this
could be a significant waste of time.Or maybe not, the instructions
are pretty simple, good thing I paid proper attention to the description this time.
Or maybe there wasn't (or I did not notice) anything tricky.
It feels a bit of a waste though that they created this machine
and then the puzzle just makes you create it by following instructions...
Let's see what part 2 has to say about this.
"""

answer_sample = solution("./sample_input.txt")
print("Answer (sample):", answer_sample)
assert(answer_sample == "4,6,3,5,6,3,5,2,1,0")

answer = solution("./input.txt")
print("Answer:", answer)
assert(answer == "7,4,2,5,1,4,6,0,4")
