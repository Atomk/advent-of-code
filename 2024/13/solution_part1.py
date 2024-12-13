"""
We're now going in the direction of math rather than
programming, I think. I admit this looks a bit out
of my comfort zone.
"""

from dataclasses import dataclass

@dataclass
class Vec2:
    x: int
    y: int

@dataclass
class MachideInfo:
    btn_a: Vec2
    btn_b: Vec2
    prize: Vec2

def day13(data_file_path) -> int:
    file = open(data_file_path)
    machines: list[MachideInfo] = []
    i = 0
    for line in file:
        match i:
            case 0:
                machines.append(MachideInfo(None, None, None))
                coordinates = line[10:].split(", ") # ["X+94", "Y+34"]
                coordinates[0] = int(coordinates[0][2:])
                coordinates[1] = int(coordinates[1][2:])
                machines[-1].btn_a = Vec2(coordinates[0], coordinates[1])
            case 1:
                coordinates = line[10:].split(", ") # ["X+94", "Y+34"]
                coordinates[0] = int(coordinates[0][2:])
                coordinates[1] = int(coordinates[1][2:])
                machines[-1].btn_b = Vec2(coordinates[0], coordinates[1])
            case 2:
                # Prize: X=8400, Y=5400
                coordinates = line[7:].split(", ")
                coordinates[0] = int(coordinates[0][2:])
                coordinates[1] = int(coordinates[1][2:])
                machines[-1].prize = Vec2(coordinates[0], coordinates[1])
            case 3:
                # Empty line
                pass
        i = (i + 1) % 4
    file.close()

    total_tokens = 0

    for machine in machines:
        # Basically, assuming A and B are vectors representing the movement
        # applied by pressing that button, and P the prize position,
        # you have to find the lowest values of 'a' and 'b' that make this equation true:
        #   A*a + B*b == P
        # Which is equivalent to:
        #   (Ax*a + Bx*b) + (Ay*a + By*b) == (Px + Py)
        # or this system:
        #   Ax*a + Bx*b == Px
        #   Ay*a + By*b == Py

        # TODO possible optimization: find if prize x or Y can be a multiple of the two buttons movement

        min_a_presses = 9999
        min_b_presses = 9999
        min_token_cost = None

        # "each button would need to be pressed no more than 100 times"
        for a in range(101):
            for b in range(101):
                if (machine.btn_a.x * a) + (machine.btn_b.x * b) == machine.prize.x:
                    if (machine.btn_a.y * a) + (machine.btn_b.y * b) == machine.prize.y:
                        tokens_cost = a*3 + b
                        if min_token_cost is None or tokens_cost < min_token_cost:
                            min_a_presses = a
                            min_b_presses = b
                            min_token_cost = tokens_cost

        # print(machine, min_token_cost, min_a_presses, min_b_presses)

        # If a successful combination was found
        if min_token_cost is not None:
            total_tokens += min_token_cost

    return total_tokens

"""
Oh, I guess bruteforce can be a good answer sometimes!
Reading the first part of the puzzle description sounded scary,
I thought it was going to be some kind of advanced math problem.

Done in 50 minutes, some spent looking for a good way to import
data for each machines. Best thing would have been to read
multiple lines at a time or read all file at once and split by "\n\n",
but I felt my implementations was good enough and moved on.

The only logic error I made was that I always added the min_token_cost
to the total, while it has to be done only if the prize can actually be reached
(meaning there is actually a min_token_cost)
"""

answer_sample = day13("./sample_input.txt")
print("Answer part 1 (sample):", answer_sample)
assert(answer_sample == 480)

answer = day13("./input.txt")
print("Answer part 1:", answer)
assert(answer == 31065)
