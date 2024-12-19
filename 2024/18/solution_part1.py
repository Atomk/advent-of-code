"""
2024-12-18
I had to skip yesterday's puzzle, did not have time to look at it.
I'll do this and then go back depending on how much time I have left.
"""

from dataclasses import dataclass

@dataclass
class Pos:
    row: int
    col: int

from collections import namedtuple
PosTup = namedtuple("PosTup", "row col")

from enum import Enum

class Direction(Enum):
    UP = Pos(-1, 0)
    RIGHT = Pos(0, 1)
    DOWN = Pos(1, 0)
    LEFT = Pos(0, -1)

DIRECTIONS = (Direction.UP, Direction.RIGHT, Direction.DOWN, Direction.LEFT)
SPACE = "."

def pathfinding_dfs(grid, row, col, width, height, steps_count):
    grid[row][col] = steps_count

    for direction in DIRECTIONS:
        next_row = row + direction.value.row
        next_col = col + direction.value.col
        if next_row < 0 or next_row >= height or next_col < 0 or next_col >= width:
            continue
        next_val = grid[next_row][next_col]
        if next_val == SPACE or steps_count + 1 < next_val:
            pathfinding_dfs(grid, next_row, next_col, width, height, steps_count + 1)


def pathfinding_dfs_close_dead_ends(grid, row, col, width, height, steps_count):
    grid[row][col] = steps_count

    walls = 0
    for direction in DIRECTIONS:
        next_row = row + direction.value.row
        next_col = col + direction.value.col
        if next_row < 0 or next_row >= height or next_col < 0 or next_col >= width:
            continue
        next_val = grid[next_row][next_col]
        if next_val == "#":
            walls += 1
            continue
        if next_val == SPACE or steps_count + 1 < next_val:
            pathfinding_dfs_close_dead_ends(grid, next_row, next_col, width, height, steps_count + 1)
            if grid[next_row][next_col] == "#":
                walls += 1
    if walls >= 3:
        grid[row][col] = "#"


def update_next_nodes(grid, row, col, width, height, steps_count, leaf_nodes_set: set):
    for direction in DIRECTIONS:
        next_row = row + direction.value.row
        next_col = col + direction.value.col
        if next_row < 0 or next_row >= height or next_col < 0 or next_col >= width:
            continue
        next_val = grid[next_row][next_col]
        if next_val == "#":
            continue
        if next_val == SPACE or steps_count + 1 < next_val:
            leaf_nodes_set.add(PosTup(next_row, next_col))

def pathfinding_bfs(grid, width, height, steps_count, leaf_nodes: set[PosTup]) -> int:
    while True:
        #print(f"Depth: {steps_count} // Leaves: {len(leaf_nodes)}")
        new_unique_leaf_nodes = set()
        for leaf in leaf_nodes:
            grid[leaf.row][leaf.col] = steps_count
            # With this algorithm the first to reach the end wins
            if leaf.row == width - 1 and leaf.col == height - 1:
                return steps_count
        for leaf in leaf_nodes:
            update_next_nodes(grid, leaf.row, leaf.col, width, height, steps_count, new_unique_leaf_nodes)
        if len(new_unique_leaf_nodes) == 0:
            # Could not reach end tile, probably
            return -1
        leaf_nodes.clear()
        leaf_nodes = new_unique_leaf_nodes
        steps_count += 1


def solution(data_file_path, max_index, input_limit) -> int:
    file = open(data_file_path)
    grid = []
    corrupted_bytes = []
    for i in range(input_limit):
        line = file.readline()
        parts = line.strip().split(",")
        byte = Pos(int(parts[1]), int(parts[0]))
        corrupted_bytes.append(byte)
    file.close()

    grid = []
    width = max_index + 1
    for i in range(width):
        row = [SPACE] * width
        grid.append(row)

    # Place obstacles
    for byte in corrupted_bytes:
        grid[byte.row][byte.col] = "#"

    # # Print map
    # for line in grid:
    #     print("".join(line))

    # Works only on sample input
    #pathfinding_dfs(grid, 0, 0, max_index+1, max_index+1, 0)
    #shortest_path_length = grid[max_index][max_index]

    shortest_path_length = pathfinding_bfs(grid, max_index+1, max_index+1, 0, set([PosTup(0, 0)]))

    return shortest_path_length

"""
The description was really confusing and I had to read some parts a couple times.
Falling bytes? What? Do they slide down in the map? I felt the need to be careful
and try with the sample data just to be sure I wasn't missing anything.
Seeing the examples, it became clear this is just another pathfinding exercise,
and an easy one at that. I know how to do this, and it's much simpler than day 16
where I failed hard the second part.
---
I initially wrote a Vec2(x, y) class but quickly realized it's much easier to work
with row/col, and I also needed directions again... I really don't want to write
the same thing again for ten days ina row, so i copied the declarations of Pos
and Direction from day 16.
This time the first thing I implemented after file load was map drawing, just to
be sure i was doing things properly. I later found this to be a bit unnecessary,
since the VSCode debugger can also show the contents of matrices on multiple lines...

40 minutes in, a lot, maybe I was distracted...
implementation was pretty easy and for the sample input, after an initial small
compilation error, the first sample passed its test first try. Then after looking
at `input.txt` I figured out what "Simulate the first kilobyte (1024 bytes)" meant...
I changed a couple things and again like day 16 I hit the max recursion limit,
I thought increasing it was enough, but after increasing it over 2500 Python
started to silently crash after a few seconds, and I was REALLY confused.
I thought this had nothing to do with my code, oh boy was I wrong...
The debugger also stopped after a few hundred iterations of my recursive function,
after raising the recursion limit to a million I started doubting reality and
slowly tried to pinpoint the problem. I know this algorithm works, there is no
obvious memory leakage so the problem might be something else.
---
After some debugging I found out that my depth-first search approach that I'm so used to
is okay for small areas (what I always used it for) but it sucks bad for big maps,
because it may fully explore the map while much more efficient routes will only be
explored later, routes that will traverse hte whole map again end overwrite anything
the first traversals did. Very inefficient.
I've never used depth-first on "big" maps so of course I did not know.
I spent some time thinking about and trying possible solutions, my first focus was "how
do I make this need less recursive calls" but I scrapped my first new attempt. Then tried
an idea that closes all dead routes but after seeing the map again it was clear this cannot
work here due to the big empty areas. So my question was the wring question, why did I want
to recycle what I have already done?
Honestly I was procrastinating breadth-first traversal because admittedly I know it exists
but i've never implemented it, I just know it exists and more or less how it works visually
on trees. It also sounded a bit more memory hungry than DPS, but now I'd say I'm not
qualified enough to make these claims yet.
(fun fact: I found out about the acronym DPS and BFS like a week ago)
As I said I had no idea how to implement it but more or less knew what it should do,
so after doing some sketches on Paint I had the big picture in mind.
---
when i thought I was done, again after letting my BFS run for a while it did not end...
what have i doe wrong this time?
Looking at the grid contents in the debugger did not help me much here, I thought something
is using way too much memory but nothing looked obviously wrong. I noticed after some
iterations things get dramatically slow. With some print debugging I found this happens
around depth 128. By aso printing the number of leaf notes it's obvious that's the problem
since it grows exponentially.
At some point in all this I realized that the list of new leaf nodes may contain duplicates
if multiple tiles share the same neighbour, but in that moment i did not think much of it,
and I still sis not think that is enough to create literally millions of nodes.
I was out of ideas though so I tried fixing that, by using a set instead of a list to track nodes.
And boom! That was it, Function finishes almost instantly.
Almost 3 hours for something not even that hard...

However, initially I had a get_next_cells() that returned a list, now it's called
update_next nodes and updates a shared set, I don't know why I did not think
of it sooner, especially since I hated the idea of creating many small disposable lists.
In the end I think I did overall a good job with BFS for a first-timer, holy crap though,
these puzzles are harsh teachers.
Left my implementations here for history (and shame)
"""

answer_sample = solution("./sample_input.txt", 6, 12)
print("Answer (sample):", answer_sample)
assert(answer_sample == 22)

# import sys
# print("Current recursion limit:", sys.getrecursionlimit())
# print("Increasing recursion limit")
# sys.setrecursionlimit(10_000)

answer = solution("./input.txt", 70, 1024)
print("Answer:", answer)
assert(answer == 278)
