"""
Holy crap this looks harder than previous days.
Let's see if I come up with something good.
"""

def isUpdateCorrect(update, rules):
    for rule in rules:
        if rule[0] in update and rule[1] in update:
            if update.index(rule[0]) > update.index(rule[1]):
                return False

    return True

def part1(data_file_path):
    file = open(data_file_path)
    rules: list[list[str]] = []
    updates: list[list[str]] = []

    for line in file:
        # Skip the newline in the middle of the file
        if len(line) < 2: continue

        if line[2] == "|":
            rules.append(line.strip().split("|"))
        else:
            updates.append(line.strip().split(","))

    file.close()

    sum_of_middles = 0

    for update in updates:
        if isUpdateCorrect(update, rules):
            middle_index = len(update) // 2
            sum_of_middles += int(update[middle_index])

    return sum_of_middles

"""
I'm very embarassed to admit it took me 35 minutes to get this right.
I thought of another solution before this one but then re-reading the text
it was clear that it could not work because a rule applies only when both numbers are present.

So, bruteforce it is, which actually makes the solution very easy,
the text only makes it sound complicated. Like previous days I made a couple
of stupid mustakes, like forgetting to remove the newline character from the line,
and latering trying to integrate the contents of isUpdateCorrect in the updates loop
when it's perfectly fine and readable to leve it as it is.

I guess as long as I exercise I will get better, with some more discipline.
"""

print("Answer 1:", part1("./sample_input.txt"))
print("Answer 1:", part1("./input.txt"))
assert(part1("./sample_input.txt") == 143)
assert(part1("./input.txt") == 5275)


# ------------------------------
# ----------  Part 2  ----------
# ------------------------------


"""
This sounded even harder than first part at first,
but I guess I can just switch the numbers with the incorrect ordering?
I don't have much time now to think this through so I'm not confident it will work but let's see.
"""

def part2(data_file_path):
    file = open(data_file_path)
    rules: list[list[str]] = []
    updates: list[list[str]] = []

    for line in file:
        # Skip the newline in the middle of the file
        if len(line) < 2: continue

        if line[2] == "|":
            rules.append(line.strip().split("|"))
        else:
            updates.append(line.strip().split(","))

    file.close()

    sum_of_middles = 0

    for update in updates:
        # Init to false just to enter the loop
        is_correct = False
        needed_fix = False
        while not is_correct:
            is_correct = True
            for rule in rules:
                if rule[0] in update and rule[1] in update:
                    index_a = update.index(rule[0])
                    index_b = update.index(rule[1])
                    if index_a > index_b:
                        is_correct = False
                        temp = update[index_a]
                        update[index_a] = update[index_b]
                        update[index_b] = temp

            if not is_correct:
                needed_fix = True

        if needed_fix:
            middle_index = len(update) // 2
            sum_of_middles += int(update[middle_index])

    return sum_of_middles

"""
Took me 23 minutes because one single swap pass wasn't enough
for some cases, which I discovered after some print debugging.
So again I went full bruteforce and added another loop to keep swapping
elements until all rules are followed.
I tried to think of a better way to reorder the updates array
but what can I say, it's not an easy problem and I like to think
if it works and it's easy to understand it's good enough (of course
in other contexts other tradeoffs need to be made but not for these puzzles)

After solving this part I added the is_correct comment
and did a tiny formatting change,
other than that I want to point out that all code is
exactly what first passed the test, usually after I get the answer
I don't add/change/refactor anything in the code
"""

print("Answer 2:", part2("./sample_input.txt"))
print("Answer 2:", part2("./input.txt"))
assert(part2("./sample_input.txt") == 123)
assert(part2("./input.txt") == 6191)