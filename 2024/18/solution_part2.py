"""
2024-12-18
Since the BFS of part 1 is pretty fast I hope this won't take as long...
"""

from collections import namedtuple
PosTup = namedtuple("PosTup", "row col")

from enum import Enum

class Direction(Enum):
    UP = PosTup(-1, 0)
    RIGHT = PosTup(0, 1)
    DOWN = PosTup(1, 0)
    LEFT = PosTup(0, -1)

DIRECTIONS = (Direction.UP, Direction.RIGHT, Direction.DOWN, Direction.LEFT)
TILE_EMPTY = "."


def update_next_nodes(grid, row, col, width, height, steps_count, leaf_nodes_set: set):
    for direction in DIRECTIONS:
        next_row = row + direction.value.row
        next_col = col + direction.value.col
        if next_row < 0 or next_row >= height or next_col < 0 or next_col >= width:
            continue
        next_val = grid[next_row][next_col]
        if next_val == "#":
            continue
        if next_val == TILE_EMPTY or steps_count + 1 < next_val:
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


def solution(data_file_path, max_index, input_limit) -> str:
    file = open(data_file_path)
    grid = []
    corrupted_bytes: list[PosTup] = []
    for line in file:
        parts = line.strip().split(",")
        byte = PosTup(int(parts[1]), int(parts[0]))
        corrupted_bytes.append(byte)
    file.close()

    grid = []
    MAP_SIZE = max_index + 1
    for i in range(MAP_SIZE):
        row = [TILE_EMPTY] * MAP_SIZE
        grid.append(row)

    # Place obstacles
    for i in range(input_limit):
        byte = corrupted_bytes[i]
        grid[byte.row][byte.col] = "#"

    # # Print map
    # for line in grid:
    #     print("".join(line))

    for i in range(input_limit, len(corrupted_bytes)):
        for r in range(MAP_SIZE):
            for c in range(MAP_SIZE):
                if grid[r][c] != "#":
                    grid[r][c] = TILE_EMPTY
        byte = corrupted_bytes[i]
        grid[byte.row][byte.col] = "#"

        shortest_path_length = pathfinding_bfs(grid, max_index+1, max_index+1, 0, set([PosTup(0, 0)]))
        if shortest_path_length == -1:
            # x,y
            return f"{byte.col},{byte.row}"

    return "---error---"

"""
FIRST TRY IN 12 MINUTES 55 SECONDS HELL YEAH!
From one extreme to the other.
I'll just update the last test and won't change anything else.
This is a glorious moment of revenge against the first part of the puzzle.

Pat on the back to myself for checking only "bytes" after the original
input limit, since we already know that value result in a successful path to the end.
I guess I was a bit lucky that in the first part I decided to make the BFS return a value,
while for the DPS I just checked the value of the end tile after the function call.
"""

answer_sample = solution("./sample_input.txt", 6, 12)
print("Answer (sample):", answer_sample)
assert(answer_sample == "6,1")

answer = solution("./input.txt", 70, 1024)
print("Answer:", answer)
assert(answer == "43,12")
