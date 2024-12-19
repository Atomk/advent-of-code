"""
2024-12-19
Looks doable, let's see.
"""


def is_possible(design: str, towel_types):
    reached_end = False

    for towel in towel_types:
        if design.startswith(towel):
            remaining_chars = design.removeprefix(towel)
            if len(remaining_chars) == 0:
                reached_end = True
            if not reached_end:
                reached_end = is_possible(remaining_chars, towel_types)

    return reached_end


def solution(data_file_path) -> int:
    file = open(data_file_path)
    towel_types: list[str] = file.readline().strip().split(", ")
    # skip empty line
    file.readline()
    designs: list[str] = []
    while True:
        line = file.readline().strip()
        if line == "":
            break
        designs.append(line)
    file.close()

    possible_designs = 0
    for design in designs:
        if is_possible(design, towel_types):
            possible_designs += 1

    return possible_designs

"""
42 minutes, yay! During first attempt I realized I was going down the wrong
path because I was just checking if you can create a design by combining
the "biggest" matching patterns, instead I had to check if ANY combination
of towels makes it possible to create the design.
My fault for not understanding the task properly, I was probably too hasty
when reading the description. So I scrapped my two unfinished implementation
attempts and decided recursion is the right solution here. Like in day 18
BFS would probably be faster since search can stop as soon as a successful
"path" is found, while in my DFS it was a bit tricky to find a way to
return True when any successful path is found.
However, everything worked first try - my first compilation attempt
gave the correct answer right away, which is pretty nice.
(actually it was the second compilation because at first I always print
loaded data to see if I parsed input correctly)
"""

answer_sample = solution("./sample_input.txt")
print("Answer (sample):", answer_sample)
assert(answer_sample == 6)

answer = solution("./input.txt")
print("Answer:", answer)
assert(answer == 233)
