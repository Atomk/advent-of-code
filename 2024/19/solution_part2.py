"""
2024-12-19
I have a neat idea to solve this quickly, let's see if that's enough.
"""


def valid_combinations_simple(design: str, towel_types) -> int:
    reached_end_count = 0

    for towel in towel_types:
        if design.startswith(towel):
            remaining_chars = design.removeprefix(towel)
            if len(remaining_chars) == 0:
                reached_end_count += 1
            else:
                reached_end_count += valid_combinations_simple(remaining_chars, towel_types)

    return reached_end_count


def valid_combinations_memo(design: str, towel_types, memoizer: dict[str, int]) -> int:
    reached_end_count = 0

    for towel in towel_types:
        if design.startswith(towel):
            remaining_chars = design.removeprefix(towel)
            if len(remaining_chars) == 0:
                reached_end_count += 1
            elif remaining_chars in memoizer:
                reached_end_count += memoizer[remaining_chars]
            else:
                combinations = valid_combinations_memo(remaining_chars, towel_types, memoizer)
                memoizer[remaining_chars] = combinations
                reached_end_count += combinations

    return reached_end_count


def solution(data_file_path) -> int:
    file = open(data_file_path)
    all_towel_types: list[str] = file.readline().strip().split(", ")
    # skip empty line
    file.readline()
    designs: list[str] = []
    while True:
        line = file.readline().strip()
        if line == "":
            break
        designs.append(line)
    file.close()

    memoizer: dict[str, int] = dict()

    #print("Total towel types:", len(all_towel_types))
    total_possible_combinations = 0
    available_towels = []
    for design in designs:
        available_towels.clear()
        for towel in all_towel_types:
            if towel in design:
                available_towels.append(towel)

        possible_combinations = valid_combinations_memo(design, available_towels, memoizer)
        total_possible_combinations += possible_combinations
        #print(memoizer)
        #print("Available towel types:", len(available_towels))
        #print(design, possible_combinations)

    # 10710 for puzzle input, that's much lower than I expected
    #print("Elements in the memoizer:", len(memoizer))
    return total_possible_combinations

"""
5 minutes in, the first test already passed but of course this
is running longer than it should, it could not be so easy.
This time I doubt it's a DFS vs. BFS, I probably missed something.
---
The only way I can think of to speed this up is limit the number
of towels (blocks that can make up a design) to only combinations
that are actually in the big string. Let's try.
---
30 minutes in (most of it spent waiting for the console to show...something)
The idea described above optimized the algorithm quite a bit, I did not realize
there are like 440 towels/patterns. That's much more than I expected.
Now the first two big strings (I cannot see data for the others yet)
will check combinations for "just" around 70 towels, but still I cannot
get past the first string, which has zero possible combinations.
The second one has been calculations for like 5 minutes and still
hasn't finished, I have to dig deeper.
---
50 minutes in, I could not come up with any other idea but now I have
one: start from the end and memoize results, so any pattern combination
is computed just once, this can skip long recursion branches if
for example two strings end with "bwrugggrgu" and we already know
that combination can be created in 35 different ways (I came up with that number)
The dictionary may become huge but I think this has potential. Let's try!
---
Around 1h5m in, holy shit it worked! Got the result almost instantly, unbelievable.
I am not completely sure exactly how it works, the combination of recursion
and memoization is not exactly easy to reason about, but this was the solution.
I did not even need to start from the end of the strings as I had planned.
No wonder I could not bruteforce the value for the second string:
the number of possible combination is 2_721_920_852. The final answer is
a number so big I don't think I could solve this in a million years in
without memoization. I came up with that number of years.
How would I get a good estimate for the number of years?
That's a good question for another puzzle., anyway it's hard to tell
since some strings are impossible to form so the calculations end
in a very short time.
I don't remember where I first heard of memoization, looking at my bookmarks
it was probably when reading some random post found on Reddit/hackernews
or in a discussion in the Zig issue tracker, probably both.
So all that procrastination wasn't all bad. Like yesterday for BFS,
I understood the big picture of memoization but this is the first time
I actually need it and use it, I'm pretty happy that I solved this puzzle
without any hint and great job to whoever designed it.
This felt like a Dark Souls boss in some ways (got to Anor Londo and
then abandoned it because life, I should revisit that too).
(note that the only time I ever searched for a hint in advent of code was
for second part of day 6, that I could not solve and did not revisit yet)
"""

answer_sample = solution("./sample_input.txt")
print("Answer (sample):", answer_sample)
assert(answer_sample == 16)

answer = solution("./input.txt")
print("Answer:", answer)
assert(answer == 691316989225259)
