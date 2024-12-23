"""
2024-12-23
Ahhhh so I have to use the harder approach with this,
which I was able to avoid in the first part.
Not really hard, just a bit annoying.
"""

Network = list[str]
def solution(data_file_path) -> str:
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

    biggest_network = []
    for network in networks:
        a = network[0]
        b = network[1]
        big_network = [a, b]
        for c in connections.keys():
            if c == a or c == b:
                continue
            all_connected = True
            for node in big_network:
                if node not in connections[c]:
                    all_connected = False
                    break
            if all_connected:
                big_network.append(c)

        if len(big_network) > len(biggest_network):
            biggest_network = big_network

    biggest_network.sort()
    return ",".join(biggest_network)

"""
Oh, much easier than I thought! Unfortunately I paused the timer to write
the initial notes in this file and forgot to reactivate it, I was
pretty fast though, I'm confident I used less than 15 minutes.
And also worked first try!
I just copypasted previous code and changed it to add a computer
to the input list if all compiters in the network are in its "connections" list.
Luckily this time there are no peformance bottlenecks it's always a bit scary
when that happens.
I don't like that both here and in the previous part there is the "network"
structure, it's handy but in the end it's just redundant data,
I think there is some opportunity for code cleanup but it's short, it works,
and takes advantage of pre-computed data (the input file) even though I
don't like special cases (if c == a or c == b: continue).
So this solution is not perfect but it's certainly good enough.
"""

answer_sample = solution("./sample_input_2.txt")
print("Answer (sample_2):", answer_sample)
assert(answer_sample == "co,de,ka,ta")

answer = solution("./input.txt")
print("Answer:", answer)
assert(answer == "bd,bu,dv,gl,qc,rn,so,tm,wf,yl,ys,ze,zr")
