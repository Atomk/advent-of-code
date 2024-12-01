import time

# It's been a while since last time I used Python, but I think right now it's my best option for these challenges.
# NOTE All numbers in both lists have the same number of digits

def part1():
    file = open("./input.txt")

    left_list = []
    right_list = []

    for line in file:
        left_list.append(int(line[:5]))
        # Specify end to exclude line terminator
        right_list.append(int(line[8:13]))

    file.close()

    left_list.sort()
    right_list.sort()

    distance_sum = 0
    for l, r in zip(left_list, right_list):
        distance_sum += abs(r - l)

    print(distance_sum)

# Pretty straightforward in Python! Executing this is so fast I won't bother looking for optimization.
# First attempt I got the wrong result because I missed abs().
# It's a distance, of course it should be always positive.
# From the sample in the prompt I thought the right number is always bigger than left number... But the text dows not said that.
# Probably they intentionally avoided showing a case where left value > right value. Distraction error!
# From beginning to end the first part took me ~30m because i also looked up some things about benchmarking, i did not mean to be as fast as possible.

def part2():
    file = open("./input.txt")

    left_list = []
    right_list = []
    dict_times: dict[int, int] = {}

    for line in file:
        left_list.append(int(line[:5]))
        # Specify end to exclude line terminator
        r = int(line[8:13])
        right_list.append(r)
        if(r in dict_times):
            dict_times[r] += 1
        else:
            dict_times[r] = 1

    file.close()

    similarity_sum = 0
    for l in left_list:
        times = dict_times[l] if l in dict_times else 0
        similarity_sum += l * times

    print(similarity_sum)

# Part 2 took me like 10-15 minutes including reading the prompt and checking correctness with sample data first.
# Got it first try, pretty easy and the examples in the prompt are of great help to clarify doubts I had reading the specs. Nice!

tstart = time.perf_counter()
#part1()
part2()
tend = time.perf_counter()
print("Time: " + str(tend - tstart) + " seconds")


