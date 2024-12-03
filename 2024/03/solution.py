import re

file = open("./input.txt")

mult_sum = 0

for line in file:
    matches: list[str] = re.findall("mul[(]\d+,\d+[)]", line)
    for match in matches:
        operands = match.removeprefix("mul(").removesuffix(")").split(",")
        mult_sum += int(operands[0]) * int(operands[1])

file.close()

# Easy! 15m, I had to had too look up a couple things about regexp (https://regex101.com/ best website ever)
# and how to use them in Python (I think I've only ever used regexp with JavaScript)
# I always start the timer before reading the puzzle description

print("Answer 1:", mult_sum)
assert(mult_sum == 188741603)


# ------------------------------
# ----------  Part 2  ----------
# ------------------------------


# This could probably be faster with a different parser that ignores all checks for "mul" if "don't()" is found

file = open("./input.txt")

mult_sum = 0
mul_enabled = True

for line in file:
    matches: list[str] = re.findall("(?:mul[(]\d+,\d+[)])|(?:do[(][)])|(?:don't[(][)])", line)
    for match in matches:
        if match == "do()":
            mul_enabled = True
            continue
        elif match == "don't()":
            mul_enabled = False
            continue
        elif mul_enabled:
            operands = match.removeprefix("mul(").removesuffix(")").split(",")
            mult_sum += int(operands[0]) * int(operands[1])

file.close()

# Another easy one, again I didn't even need to test against the sample input, I was that confident.
# Did it in 10m, this time the tricky part was that I never used capturing groups
# and my first regexp looked like this:
# (mul[(]\d+,\d+[)])|(do[(][)])|(don't[(][)])
# Notice the lack of "?:"
# This resulted in Python returning "matches" formed like this:
# ('mul(450,613)', '', ''), ('mul(983,770)', '', ''), ('', 'do()', ''), ...
# I'll need to read something about this, apparently I needed "non-capturing groups", which is exactly why "?:" is needed:
# Problem solved thanks to: https://python-forum.io/thread-32588-post-137760.html#pid137760

print("Answer 2:", mult_sum)
assert(mult_sum == 67269798)