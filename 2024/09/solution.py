"""
It took me a bit to make sure I understood the task,
it's not complicated but there are come steps to think about.
This is another case of "should I bruteforce it",
I think the "compact" step can be skipped but since
this thought already stinged me in at least a couple of previous puzzle,
I think I'll take the easy expensive route and go from there.
"""

def part1(data_file_path) -> int:
    file = open(data_file_path)
    # NOTE strip returns a clone, not ideal for a big string
    input = file.read().strip()
    file.close()

    blocks = []
    numbers_count = 0
    file_id = 0
    i = 0
    for char in input:
        amount = int(char)
        if i % 2 == 0:
            blocks.extend([file_id] * amount)
            numbers_count += amount
            file_id += 1
        else:
            blocks.extend(["."] * amount)
        i += 1

    checksum = 0
    last = len(blocks) - 1
    for i in range(numbers_count):
        if blocks[i] != ".":
            checksum += i * blocks[i]
        else:
            # Make last index point to "next" number from the end of the file
            while blocks[last] == ".":
                last -= 1
            checksum += i * blocks[last]
            last -= 1

    return checksum

"""
35 minutes, it was a bit less trickier than I expected.
In the end I used the optimization I had in mind, use one single loop
to calculate the checksum instead of having two different passes.
Let's hope this shortcut does not bite too hard in the second part.
"""

print("Answer part 1 (sample):", part1("./sample_input.txt"))
assert(part1("./sample_input.txt") == 1928)
print("Answer part 1:", part1("./input.txt"))
assert(part1("./input.txt") == 6471961544878)

