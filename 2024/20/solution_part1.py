"""
2024-12-23
Le0ts see if I can sqeeze in this one too today, I've just completed
day 23 but this is one of the two puzzles I did not have time to look
at yet. I hope I can do this fast so I can have all puzzles with
at least one star by Christmas.
---
Crap, it's a bit tricky, but an interesting take on the usual
grid traversal that I'm starting to find a bit boring.
Good news is, probably here there's no difference between DFS and BFS.
"""

from collections import namedtuple
PosTup = namedtuple("PosTup", "row col")

from dataclasses import dataclass

@dataclass
class Pos:
    row: int
    col: int

from enum import Enum

class Direction(Enum):
    UP = Pos(-1, 0)
    DOWN = Pos(1, 0)
    LEFT = Pos(0, -1)
    RIGHT = Pos(0, 1)

DIRECTIONS = [Direction.UP, Direction.RIGHT, Direction.DOWN, Direction.LEFT]

def find_noclip_locations(grid, pos: PosTup, already_visited: set[PosTup], locations: set[PosTup]):
    already_visited.add(pos)

    for direction in DIRECTIONS:
        next_pos = PosTup(pos.row + direction.value.row, pos.col + direction.value.col)
        if next_pos in already_visited:
            continue
        match grid[next_pos.row][next_pos.col]:
            case "#":
                after_wall = PosTup(next_pos.row + direction.value.row, next_pos.col + direction.value.col)
                if in_bounds(after_wall, grid):
                    if grid[after_wall.row][after_wall.col] == ".":
                        # if next_pos not in locations:
                        locations.add(next_pos)
            case "E": return
            case ".": find_noclip_locations(grid, next_pos, already_visited, locations)

def find_noclip_locations_flat(grid, pos: PosTup, already_visited: set[PosTup], locations: set[PosTup]):
    after_wall_allowed = (".", "E")
    next_walkable_pos = PosTup(-1, -1)
    while True:
        already_visited.add(pos)
        for direction in DIRECTIONS:
            next_pos = PosTup(pos.row + direction.value.row, pos.col + direction.value.col)
            if next_pos in already_visited:
                continue
            match grid[next_pos.row][next_pos.col]:
                case "#":
                    after_wall = PosTup(next_pos.row + direction.value.row, next_pos.col + direction.value.col)
                    if in_bounds(after_wall, grid):
                        if grid[after_wall.row][after_wall.col] in after_wall_allowed:
                            locations.add(next_pos)
                case "E": return
                case ".": next_walkable_pos = next_pos
        # It's important for 'pos' to be mutated outside directions loop
        # because 'next_pos' depends on it
        pos = next_walkable_pos


def in_bounds(pos: PosTup, grid):
    return pos.row >= 0 and pos.col >= 0 and pos.row < len(grid) and pos.col < len(grid[0])

def traverse_dfs(grid, pos: PosTup, steps, already_visited: set[PosTup], steps_to_end):
    already_visited.add(pos)

    for direction in DIRECTIONS:
        next_pos = PosTup(pos.row + direction.value.row, pos.col + direction.value.col)

        if next_pos in already_visited:
            continue
        if next_pos.row < 1 or next_pos.col < 1 or next_pos.row >= len(grid) or next_pos.col >= len(grid[0]):
            continue

        match grid[next_pos.row][next_pos.col]:
            case "#":
                #if can_noclip and next_pos not in noclip_tried_locations
                continue
                after_wall = PosTup(next_pos.row + direction.value.row, next_pos.col + direction.value.col)
                if in_bounds(after_wall, grid) and grid[after_wall.row][after_wall.col] == ".":
                    traverse_dfs(grid, next_pos, steps + 1, already_visited, steps_to_end)
            case "E":
                steps_to_end.append(steps + 1)
                return
            case ".": traverse_dfs(grid, next_pos, steps + 1, already_visited, steps_to_end)

# Advantage over DFS is it's easier to stop traversal as soon as end is reached
def traverse_bfs(grid, pos: PosTup, already_visited: set[PosTup], noclip_pos: PosTup):
    steps = 0
    leaf_nodes: set[PosTup] = set([pos])
    while True:
        new_leaf_nodes = set()
        for node in leaf_nodes:
            already_visited.add(node)
            for direction in DIRECTIONS:
                next_pos = PosTup(node.row + direction.value.row, node.col + direction.value.col)
                if next_pos in already_visited:
                    continue
                match grid[next_pos.row][next_pos.col]:
                    case "#":
                        if next_pos == noclip_pos:
                            new_leaf_nodes.add(next_pos)
                    case "E": return steps + 1
                    case ".": new_leaf_nodes.add(next_pos)

        leaf_nodes = new_leaf_nodes
        steps += 1


def parse(file_path):
    file = open(file_path)
    start_pos: PosTup = None # type: ignore
    end_pos: PosTup = None # type: ignore
    grid = []
    row = 0
    for line in file:
        grid.append(list(line.strip()))
        col = 0
        for cell in grid[row]:
            match cell:
                case "S": start_pos = PosTup(row, col)
                case "E": end_pos = PosTup(row, col)
            col += 1
        row += 1
    file.close()

    return grid, start_pos, end_pos

def solution(data_file_path) -> int:
    grid, start, end = parse(data_file_path)

    # key: time saved // value = count
    dict_time_saved: dict[int, int] = dict()

    # result = []
    # traverse_dfs(grid, start, 0, set(), result)
    # assert(result == [84])

    noclip_locations = set()
    find_noclip_locations_flat(grid, start, set(), noclip_locations)
    print(len(noclip_locations))

    # assert(traverse_bfs(grid, start, set(), PosTup(-1, -1)) == 84)

    base_race_time = traverse_bfs(grid, start, set(), PosTup(-1, -1))
    i = 0
    for location in noclip_locations:
        race_time = traverse_bfs(grid, start, set(), location)
        time_saved = base_race_time - race_time
        if time_saved not in dict_time_saved:
            dict_time_saved[time_saved] = 1
        else:
            dict_time_saved[time_saved] += 1
        print(i, race_time)
        i+=1

    # print(dict_time_saved)
    count = 0
    for time_saved, amount in dict_time_saved.items():
        if time_saved >= 100:
            count += amount
    return count

"""
I challenged myself to not look at previous solutions, so everything
here is implementend from scratch from memory. Pos and Direction
are especially useful abstraction and I wrote them several times,
so I remember them pretty well. Not that they are hard to implement,
but also the choice of data structure makes a difference, for example
using row/col instead of x/y, using enums instead of manual checks, using
a list of direction (even though I could access that directly from enum fields),
using a dataclass for Pos instead of a tuple. These details matter, especially
because I already made mistakes that made me waste some time, like figuring
out the my choice of data structures made the code hard to read.
---
i hit recursion liimt, i raise it but i have silent crash. this already happended---
good thing i took notes, by reading how i solved it it looks like i had poblem with dps...
in this case my search for nocilip location. I also made again the mistake of using a list and not a set fot new_leaf_nodes
---
2h41m, these algorithms are full of traps.
Luckily the first successful compilation returned the correct answer, because it took 2-3 minutes to caculate it
---
just looked  at sexond part, i dont think i can do this,
i "cheated" with my approach to go through walls but I
have to change the strategy drastically for seconf part.
Also, my solution for part1 is really slow, I dont think i can
get to a solution for such an increased complexity in a reasonable time, i wwould have
to rethink some thongs from scratch and at hte moment i dontave any idea
"""

# answer_sample = solution("./sample_input.txt")
# print("Answer (sample):", answer_sample)
# assert(answer_sample == None)

# import sys
# sys.setrecursionlimit(50000)

answer = solution("./input.txt")
print("Answer:", answer)
assert(answer == 1387)

