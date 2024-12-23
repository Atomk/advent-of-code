"""
2024-12-23
Short description, I like.
Not super-easy but I just need to find a way to
do this in a reasonable amount of passes.
"""

Network = list[str]
def solution(data_file_path) -> int:
    # All combinations of 2 connected computers.
    networks: list[Network] = []
    # key: a computer, value: all other computers connected to this one
    connections: dict[str, set[str]] = dict()

    file = open(data_file_path)
    for line in file:
        parts = line.strip().split("-")
        computerA = parts[0]
        computerB = parts[1]
        networks.append([computerA, computerB])
        if computerA not in connections:
            connections[computerA] = set()
        if computerB not in connections:
            connections[computerB] = set()
        connections[computerA].add(computerB)
        connections[computerB].add(computerA)
    file.close()

    count = 0
    # for computer, connected_set in connections.items():
    #     if len(connected_set) < 2:
    #         continue
    #     # for pc_2 in connected_set:
    #   # if computerA.startswith("t") or computerB.startswith("t"):

    found_set = set()
    for network in networks:
        a = network[0]
        b = network[1]
        has_t = a.startswith("t") or b.startswith("t")
        for c in connections.keys():
            if c == a or c == b:
                continue
            if c.startswith("t") or has_t:
                if a in connections[c] and b in connections[c]:
                    # Make sure it's the first time we find a combination
                    # of these 3 computers
                    seq_list = [a, b, c]
                    seq_list.sort()
                    # Alternative with string:
                    # seq_key = "-".join(seq_list)
                    seq_tuple = tuple(seq_list)
                    if seq_tuple not in found_set:
                        count += 1
                        found_set.add(seq_tuple)

    return count

"""
Exactly 34 minutes, too long but better then my latest times for sure.
Wasted a bit of time at first because I wrote the "netwoek" abstraction
then though it would be better to just use "connections" and then realized
using just "connections" is complicated and it's necessary to use both.
I did not delete/rewrite anything in the process, I just needed a moment
to figure out how to actually search for all combinaiton of three computers
connected with each other.
"""

answer_sample = solution("./sample_input.txt")
print("Answer (sample):", answer_sample)
assert(answer_sample == 7)

answer = solution("./input.txt")
print("Answer:", answer)
assert(answer == 1194)
