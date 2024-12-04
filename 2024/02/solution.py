def part1(data_file_path):
    file = open(data_file_path)
    safe_count = 0

    for report in file:
        levels = [int(num) for num in report.split()]
        i = 0
        is_increasing = levels[i] < levels[i + 1]
        safe = True
        while i < len(levels) - 1:
            if levels[i] == levels[i + 1]:
                safe = False
                break
            elif is_increasing:
                if not (1 <= levels[i + 1] - levels[i] <= 3):
                    safe = False
                    break
            else:
                if not (1 <= levels[i] - levels[i + 1] <= 3):
                    safe = False
                    break
            i += 1

        if safe:
            safe_count += 1

    return safe_count

assert(part1("./sample_input.txt") == 2)
assert(part1("./input.txt") == 516)
# print("Answer:", part1("./input.txt"))

# This took me 35 minutes including reading the prompt, gosh I was slower than expected.
# I think I could have done it in 20 min with less wondering "is this the best way to do it"
# and more Python knowledge (I had to look a couple things up for splitting)
# I was tricked by the list initially being strings and not numbers, this is where typed languages clearly win
# The I forgot to put the "not" in the conditions to break the levels loop, I spent some time thinking what could be the best way to write those checks
# Let's do part 2


def part2(data_file_path):
    file = open(data_file_path)
    safe_count = 0

    for report in file:
        levels = [int(num) for num in report.split()]
        i = 0
        is_increasing = levels[i] < levels[i + 1]
        safe = True
        already_skipped_one = False
        while i < len(levels) - 1:
            if levels[i] == levels[i + 1]:
                safe = False
            elif is_increasing:
                if not (1 <= levels[i + 1] - levels[i] <= 3):
                    safe = False
            else:
                if not (1 <= levels[i] - levels[i + 1] <= 3):
                    safe = False

            if not safe:
                if already_skipped_one:
                    break
                else:
                    #if (i + 1) == len(levels) - 1:
                    levels.pop(i)
                    already_skipped_one = True
                    continue

            i += 1

        if safe:
            safe_count += 1

    return safe_count

# NOTE This does not work, I know the reason (when there's an error I remove the current item but maybe the problem is in the next one)
# but I was really tired and fell asleep while thinking up a proper solution
# I understood the assignment incorrectly and I also lost some time on premature optimization
# I'll put this on hold so I can work on day 3 but I'm sure I can solve this in the optimal way
# If it turns out to be unreadable I'll just brute-force it, we can accept compromises

assert(part2("./sample_input.txt") == 4)
print("Answer:", part2("./input.txt"))
