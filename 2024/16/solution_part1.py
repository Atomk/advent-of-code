"""
2024-12-16
Again, a pathfinding puzzle, a slightly tricky one
because we must consider all possible paths and just
accept the one with the lowest score.
As with one the the first puzzles, decompiling Ancient Empires
let me explore this kind of stuff... I guess it's a common
technique, but there after selecting a unit they create a new grid
the same size of the map, and they recursively explore paths and save
in the grid cells the movement points remaining after a unit reaches
the corresponding location.
Then to actually find the best path they go from the the destination
tile to the source tile, always choosing the neighbouring tile with the
highest value (the shortest path is where the value grows most rapidly)
I guess I can do something similar, even though it feels a bit like cheating,
I'm sure I'll have to change it anyway but I want to put at least some
creativity in the solution, otherwise the puzzles are not that entertaining.
"""

from dataclasses import dataclass

@dataclass
class Pos:
    row: int
    col: int

from enum import Enum

class Direction(Enum):
    UP = Pos(-1, 0)
    RIGHT = Pos(0, 1)
    DOWN = Pos(1, 0)
    LEFT = Pos(0, -1)

DIRECTIONS = (Direction.UP, Direction.RIGHT, Direction.DOWN, Direction.LEFT)

def pathfinding(grid, width, height, facing, row, col, score: int, final_scores: list[int]):
    grid[row][col] = score

    disallowed_direction = None
    match facing:
        case Direction.UP: disallowed_direction = Direction.DOWN
        case Direction.RIGHT: disallowed_direction = Direction.LEFT
        case Direction.DOWN: disallowed_direction = Direction.UP
        case Direction.LEFT: disallowed_direction = Direction.RIGHT

    for direction in DIRECTIONS:
        if direction == disallowed_direction:
            continue
        next_row = row + direction.value.row
        next_col = col + direction.value.col
        # row and col with index 0 are always walls
        if 0 < next_row < height and 0 < next_col < width:
            next_tile_value = grid[next_row][next_col]
            if next_tile_value == "#":
                continue

            new_score = score + 1
            if facing != direction:
                new_score += 1000

            if next_tile_value == ".":
                pathfinding(grid, width, height, direction, next_row, next_col, new_score, final_scores)
            elif next_tile_value == "E":
                # global lowest_score
                # if score + score_increment < lowest_score:
                #     lowest_score = score + score_increment
                final_scores.append(new_score)
            elif new_score < next_tile_value:
                pathfinding(grid, width, height, direction, next_row, next_col, new_score, final_scores)

def solution(data_file_path) -> int:
    file = open(data_file_path)
    grid = []
    for line in file:
        grid.append(list(line.strip()))
    file.close()

    WIDTH = len(grid)
    HEIGHT = len(grid[0])
    tile_start = Pos(HEIGHT-2, 1)
    tile_end = Pos(1, WIDTH-2)
    assert(grid[tile_start.row][tile_start.col] == "S")
    assert(grid[tile_end.row][tile_end.col] == "E")

    scores = []
    pathfinding(grid, WIDTH, HEIGHT, Direction.RIGHT, tile_start.row, tile_start.col, 0, scores)

    return min(scores)

"""
I wasted some time because I changed my mind a couple times
while choosing how to implement the "pathfinding".
At first compilation no test passed because I thought I could
avoid saving values in the map, but actually it's necessary
because otherwise some configurations can cause infinite recursion
by exploring already walked paths. So like for terrain pathfinding
(the "how far can you move" type) I saved the score value for reaching each tile
and stop recursion if we already reached a tile with a lower score.
So, after one hour in, first test passes but the second fails. What? Why?
---
Ohh, got it. I used a global lowest_score to store the lowest scoring path,
but it wasn't reset between tests, I guess that's why everyone hates globals.
Honestly I never use them, now I remember the reason I guess.
I left some of the old code commented for shame.
I used a global because it didn't seem possible to return that number
from the function, as I need to find all paths before returning, "if only
I could use a reference type"... So after the long waited lightbulb moment,
I added a list parameter, so the method still does not return anything but it works.
Ar 1h10m, second test passes.
Now the last test fails with exceeded recursion depth. What? Why?
Is the map too big for recursion?
---
Took me 1h50m holy crap, I looked at my pathfinding implementation
for a while to see if I missed something...but I concluded my implementation
is okay, the only performance "smell" is that I don't have a way to stop a path
from being explored further if another path can reach one of its points with
the same facing and a lower score. That means that a portion of a path can be
explored multiple times. It's not an easy problem to solve though, for every tile
I'd have to track the path it belongs to, or use a kind of breadth-first search
(instead of the depth-first I'm using here) where path traversal stops at a node
and when we find all paths that can reach that node we continue only with the
most optimal one. This is the most efficient solution I can think of,
but it's complex and I don't want to spend other two hours on this.
So after pondering my options for longer than I expected, I decided
I want to first try to bruteforce it all the way. It's the first time
I have to do this, but I increased the recursion limit from the default (1000)
to 2000. Well, that worked. I was almost going to call this a useless waste of time
but I must say I learned something, so it's experience.
"""

answer_sample = solution("./sample_input.txt")
print("Answer (sample):", answer_sample)
assert(answer_sample == 7036)

answer_sample = solution("./sample_input_2.txt")
print("Answer (sample_2):", answer_sample)
assert(answer_sample == 11048)

import sys
# print("Current recursion limit:", sys.getrecursionlimit())
print("Increasing recursion limit")
sys.setrecursionlimit(2000)

answer = solution("./input.txt")
print("Answer:", answer)
assert(answer == 143580)
