"""
I split the file from part 1 of the puzzle because I
had to change a field in the Trailhead class. so I could not
reuse that implementation.
"""

from collections import namedtuple
Pos = namedtuple("Pos", "row col")

from dataclasses import dataclass

@dataclass
class Trailhead:
    row: int
    col: int
    score: 0

def pathfinding(grid, th: Trailhead, row, col):
    WIDTH = len(grid)
    HEIGHT = len(grid[0])

    if grid[row][col] == 9:
        th.score += 1
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
                trailheads.append(Trailhead(row, col, 0))
            col += 1
        row += 1
    file.close()

    scores_sum = 0
    for th in trailheads:
        pathfinding(grid, th, th.row, th.col)
        scores_sum += th.score

    return scores_sum

"""
It took me like, 3 minutes? I literally just renamed
the trail field "ends" (a set of positions) to "score" (an int)
and changed only the 4 lines that accessed or updated that field.
Was I lucky again?
What is the different approach that makes this second part hard?
"""

# The puzzle does not give the exact answer to this but should be 16
# answer_sample_1 = part1("./sample_input_1.txt")
# print("Answer part 2 (sample_1):", answer_sample_1)
# assert(answer_sample_1 == ???)

answer_sample_2 = part1("./sample_input_2.txt")
print("Answer part 2 (sample_2):", answer_sample_2)
assert(answer_sample_2 == 81)

answer = part1("./input.txt")
print("Answer part 2:", answer)
assert(answer == 1942)
