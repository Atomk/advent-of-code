"""
Second attempt at solving the second part of the puzzle.
You can find the first attempt with notes in "solution.py"
"""

def is_safe(levels: list[int]):
    i = 0
    is_increasing = levels[i] < levels[i + 1]

    while i < len(levels) - 1:
        if levels[i] == levels[i + 1]:
            return False
        elif is_increasing:
            if not (1 <= levels[i + 1] - levels[i] <= 3):
                return False
        else:
            if not (1 <= levels[i] - levels[i + 1] <= 3):
                return False

        i += 1

    return True


def part2(data_file_path):
    file = open(data_file_path)
    safe_count = 0

    for report in file:
        levels = [int(num) for num in report.split()]

        # This is not necessary for correctness but since around half of cases in part 1
        # were safe, it should save some computation
        if is_safe(levels):
            safe_count += 1
            continue

        index_to_skip = 0
        while index_to_skip < len(levels):
            copy = levels.copy()
            copy.pop(index_to_skip)

            if is_safe(copy):
                safe_count += 1
                break

            index_to_skip += 1

    return safe_count


assert(part2("./sample_input.txt") == 4)
print("Answer 2:", part2("./input.txt"))
assert(part2("./input.txt") == 561)

"""
Finally done!

In the end I chose the simple brute-force option,
this solutions kinda sucks for performance with all the copies, but it is very readable.

My other idea was to keep the single.function structure of my first attempt at part 2,
but use a index_to_skip and instead of indexing with "i", use two variables "curr" and "next"
to store current and next index. I should also have changed how "is_increasing" is assigned
since it has to use "curr" and "next" too. This solution would work without copies
so in theory it should be close to the optimal solution.

I don't remember how much time I took to solve this part,
I think a little more than an hour summing both attempts;
for this specific attempt I decided to not track minutes
to give myself all the time I needed to make sure I understood
everything and implemented properly what I had in mind.
The fact I was not falling asleep on the keyboard helped :D
"""
