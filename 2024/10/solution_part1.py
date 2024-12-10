"""
Yay pathfinding! I looked at something similar recently while
decompiling Ancient Empires (old tile-based J2ME game).
I've seen this implemented with recursion but I think I
can try to use an infinite loop, let's see.
(EDIT: no it has to be recursive because any tile can lead to multiple paths)

I have a doubt though, what if from a trailhead there are two paths that
go to the same end? I guess that's one point and not two.
(EDIT: confirmed, I had to read more carefully because one of the first
sections says to count "hiking paths" but then there is a specific example
showing how multiple paths reaching the same destination count as one point)
"""

from collections import namedtuple
Pos = namedtuple("Pos", "row col")

from dataclasses import dataclass

@dataclass
class Trailhead:
    row: int
    col: int
    ends: set[Pos]

def pathfinding(grid, th: Trailhead, row, col):
    WIDTH = len(grid)
    HEIGHT = len(grid[0])

    if grid[row][col] == 9:
        th.ends.add(Pos(row, col))
        return

    tile = grid[row][col]
    if row + 1 < HEIGHT:
        if grid[row+1][col] == tile + 1:
            pathfinding(grid, th, row+1, col)
    if row - 1 >= 0:
        if grid[row-1][col] == tile + 1:
            pathfinding(grid, th, row-1, col)
    if col + 1 < WIDTH:
        if grid[row][col+1] == tile + 1:
            pathfinding(grid, th, row, col+1)
    if col - 1 >= 0:
        if grid[row][col-1] == tile + 1:
            pathfinding(grid, th, row, col-1)


def part1(data_file_path) -> int:
    file = open(data_file_path)
    grid = []
    trailheads: list[Trailhead] = []
    row = 0
    for line in file:
        stripped_line = line.strip()
        grid.append([int(char) for char in stripped_line])
        col = 0
        for n in grid[row]:
            if n == 0:
                trailheads.append(Trailhead(row, col, set()))
            col += 1
        row += 1
    file.close()

    scores_sum = 0
    for th in trailheads:
        pathfinding(grid, th, th.row, th.col)
        scores_sum += len(th.ends)

    return scores_sum

"""
Fairly easy, done in 30 minutes without any error,
I just needed some time to find a good structure for the pathfinding
and I had to change how to calc score because initially
trailhead had a "score" field but then after re-reading
"the spec" I realized I needed to track reachable positions so
that each reachable end counts as one point
I included two sample inputs because the first one would make
this bug obvious and I wanted to make sure That test passed,
I certainly didn't want to risk spending again an hour debugging
what's wrong wih the bigger data input.
"""

answer_sample_1 = part1("./sample_input_1.txt")
print("Answer part 1 (sample_1):", answer_sample_1)
assert(answer_sample_1 == 1)

answer_sample_2 = part1("./sample_input_2.txt")
print("Answer part 1 (sample_2):", answer_sample_2)
assert(answer_sample_2 == 36)

answer = part1("./input.txt")
print("Answer part 1:", answer)
assert(answer == 796)
