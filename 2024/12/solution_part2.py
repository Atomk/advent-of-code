"""
Here the examples were pretty extensive, Without those
I would not have realized that this part can be tricky.
The RegionInfo object wins here, it was definitely the right abstraction.
I'll put a list of fences inside of that (including direction top/bottom/right/left)
and then I'll check that after the function returns, each checked element
will be removed. Removal can be expensive so I doubt this is the best solution.
"""

from collections import namedtuple
Pos = namedtuple("Pos", "row col")

class RegionInfo:
    area: int
    fences: dict[Pos, set[str]]

    def __init__(self):
        self.area = 0
        self.fences = dict()

    def addFence(self, row, col, direction):
        pos = Pos(row, col)
        if pos not in self.fences:
            self.fences[pos] = set()
        self.fences[pos].add(direction)

def traverse_region(grid: list[list[str]], row, col, visited: list[list[bool]], region_info: RegionInfo):
    HEIGHT = len(grid)
    WIDTH = len(grid[0])

    region_info.area += 1
    visited[row][col] = True
    plant = grid[row][col]

    next_row = row + 1
    if next_row < HEIGHT:
        if grid[next_row][col] == plant:
             if not visited[next_row][col]:
                traverse_region(grid, next_row, col, visited, region_info)
        else:
            region_info.addFence(row, col, "bottom")
    else:
        region_info.addFence(row, col, "bottom")

    next_row = row - 1
    if next_row >= 0:
        if grid[next_row][col] == plant:
             if not visited[next_row][col]:
                traverse_region(grid, next_row, col, visited, region_info)
        else:
            region_info.addFence(row, col, "top")
    else:
        region_info.addFence(row, col, "top")

    next_col = col + 1
    if next_col < WIDTH:
        if grid[row][next_col] == plant:
             if not visited[row][next_col]:
                traverse_region(grid, row, next_col, visited, region_info)
        else:
            region_info.addFence(row, col, "right")
    else:
        region_info.addFence(row, col, "right")

    next_col = col - 1
    if next_col >= 0:
        if grid[row][next_col] == plant:
             if not visited[row][next_col]:
                traverse_region(grid, row, next_col, visited, region_info)
        else:
            region_info.addFence(row, col, "left")
    else:
        region_info.addFence(row, col, "left")

def get_sides(fences_dict: dict[Pos, set[str]]) -> int:
    sides = 0
    DIRECTIONS = ["top", "bottom", "left", "right"]
    row_increment = 0
    col_increment = 0
    while len(fences_dict) > 0:
        # The idea is to take one fence (we don't care which one),
        # make that count as a side,
        # and remove from the dictionary all other adjacent fences
        # of the same type (which means they are part of the same side),
        # so all data about this side is removed and counted only once
        fence_pos, fence_directions = next(iter(fences_dict.items()))
        for direction in DIRECTIONS:
            if direction not in fence_directions:
                continue
            sides += 1
            if direction == "top" or direction == "bottom":
                row_increment = 0
                col_increment = 1
            else:
                row_increment = 1
                col_increment = 0
            col = fence_pos.col
            row = fence_pos.row
            while True:
                row += row_increment
                col += col_increment
                pos = Pos(row, col)
                if pos in fences_dict and direction in fences_dict[pos]:
                    fences_dict[pos].remove(direction)
                    if len(fences_dict[pos]) == 0:
                        fences_dict.pop(pos)
                else:
                    break
            # now check in the opposite direction
            col = fence_pos.col
            row = fence_pos.row
            while True:
                row -= row_increment
                col -= col_increment
                pos = Pos(row, col)
                if pos in fences_dict and direction in fences_dict[pos]:
                    fences_dict[pos].remove(direction)
                    if len(fences_dict[pos]) == 0:
                        fences_dict.pop(pos)
                else:
                    break
            fences_dict[fence_pos].remove(direction)
        fences_dict.pop(fence_pos)

    return sides

def part2(data_file_path) -> int:
    file = open(data_file_path)
    grid = []
    for line in file:
        grid.append(list(line.strip()))
    file.close()

    HEIGHT = len(grid)
    WIDTH = len(grid[0])

    grid_visited = [False] * HEIGHT
    for i in range(HEIGHT):
        grid_visited[i] = [False] * WIDTH

    price_total = 0
    row = 0
    while row < HEIGHT:
        col = 0
        while col < WIDTH:
            if not grid_visited[row][col]:
                region_info = RegionInfo()
                traverse_region(grid, row, col, grid_visited, region_info)
                sides = get_sides(region_info.fences)
                price_total += region_info.area * sides
            col += 1
        row += 1

    return price_total

"""
1 hour 30 minutes.
*sigh*

For a bit I was wondering if I used the right structure to save fences.
I could also have used a list with single items, it would have been easier
to reason about, but instead of expensive O(n) removals from list in that case
I would have marked already checked fences so I could skip them easily.
Something like this:
for i in range(len(fences)):
	if already_checked[i]:
		continue
That said, regions are not that big, so even removals from a list
should not be that big of a deal, but I still think my approach
with a dictionary of positions has its merits.

As you can see I spent some time playing with ideas and wondering
how to save fences to make processing them easier and faster.

For directions I really should have used enums instead of strings...
Especially because on a line I wrote "botttom" with 3 't' and that
was a bug waiting to happen.

Also in get_sides() I has some technical difficulties and needed
a couple attempts before finding a control flow that felt good.

When it came to actual compilation, I found two bugs.
One was a copy-paste error in row_increment that kept the original value,
and the only logic error was that I forgot to also remove the
"reference" fence at the end of each iteration of the loop.
With this in particular I wasted at least 10-15 minutes by wrestling with
the VSCode debugger, which was giving some "file not found" errors.
To be fair this was the first time I used the VScode debugger for Python
(which is actually really useful) and it was a bit unexpected.
"""

answer_sample = part2("./sample_input_1.txt")
print("Answer part 1 (sample 1):", answer_sample)
assert(answer_sample == 80) # A to E: 16, 16, 32, 4, and 12

answer_sample = part2("./sample_input_2.txt")
print("Answer part 1 (sample 2):", answer_sample)
assert(answer_sample == 436)

answer = part2("./input.txt")
print("Answer part 1:", answer)
assert(answer == 886364)
