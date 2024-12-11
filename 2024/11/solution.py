"""
Sounds easy (after the scary first part of the explanation),
the choice of data structure is crucial though.
It could be a tree, or I could create a new list for each pass,
the first option is a bit more complicated while the other is
more expensive. I could also modify the original list in-place
but I'm pretty sure it would be less performant with all the O(n) insertions,
it uses less memory than creating a new list for each iteration though
(time paused while writing this)
"""

import time

def part1(data_file_path) -> int:
    perf_start = time.perf_counter()

    file = open(data_file_path)
    input = file.read().strip()
    file.close()
    stones = [int(n) for n in input.split()]

    blinks = 25
    while blinks > 0:
        temp = []
        for num in stones:
            if num == 0:
                temp.append(1)
                continue
            if num >= 10:
                num_string = str(num)
                if len(num_string) % 2 == 0:
                    HALF_INDEX = len(num_string) // 2
                    left_half = num_string[0:HALF_INDEX]
                    right_half = num_string[HALF_INDEX:]
                    temp.append(int(left_half))
                    temp.append(int(right_half))
                    continue
            temp.append(num * 2024)
        stones = temp
        blinks -= 1

    perf_result = time.perf_counter() - perf_start
    print(f"Time: {perf_result:.5f} sec")

    return len(stones)

"""
I was interrupted by a meeting and dinner but total stopwatch time
is 25 minutes, a fairly easy problem and computation time
is < 0.5 seconds (did not measure it) so I guess my intuition
may have been correct. Honestly my time sounds way too high,
I have have forgotten to stop timer while I was trying the
Python REPL in VSCode, I had to little mistakes (using "normal"
float division to calc the half index, forgetting to decrease
counter each cycle) but they were easily caught at compile time.
"""

answer_sample = part1("./sample_input.txt")
print("Answer part 1 (sample):", answer_sample)
assert(answer_sample == 55312)

answer = part1("./input.txt")
print("Answer part 1:", answer)
assert(answer == 191690)

