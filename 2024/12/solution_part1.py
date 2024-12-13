"""
The description is a bit convoluted, this is another kind of
pathfinding exercise with some complication that I need to
figure out. I need to track which regions I have already checked
and ensure any tile is walked on exactly once
(I can use a set of visited locations or a second big map, I'll do with set first)
I could copy the other pathfinding solutions but I prefer to do it by hand
since I'm using these challenges also as an exercise.
"""

from dataclasses import dataclass
@dataclass
class RegionInfo:
    area: int
    perimeter: int

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
            region_info.perimeter += 1
    else:
        region_info.perimeter += 1

    next_row = row - 1
    if next_row >= 0:
        if grid[next_row][col] == plant:
             if not visited[next_row][col]:
                traverse_region(grid, next_row, col, visited, region_info)
        else:
            region_info.perimeter += 1
    else:
        region_info.perimeter += 1

    next_col = col + 1
    if next_col < WIDTH:
        if grid[row][next_col] == plant:
             if not visited[row][next_col]:
                traverse_region(grid, row, next_col, visited, region_info)
        else:
            region_info.perimeter += 1
    else:
        region_info.perimeter += 1

    next_col = col - 1
    if next_col >= 0:
        if grid[row][next_col] == plant:
             if not visited[row][next_col]:
                traverse_region(grid, row, next_col, visited, region_info)
        else:
            region_info.perimeter += 1
    else:
        region_info.perimeter += 1


def part1(data_file_path) -> int:
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
                region_info = RegionInfo(0, 0)
                traverse_region(grid, row, col, grid_visited, region_info)
                #print(grid[row][col], region_info)
                price_total += region_info.area * region_info.perimeter
            col += 1
        row += 1

    return price_total

"""
Done in 55 minutes, I had to redo some things because halfway
I found out I incorrectly thought one plan could appear just once
in the map, I guess I was confused by the meaning of "garden plots"
and regions since I thought they were the same thing and each tile
represented a plant, while a tile is in fact a garden plot, and
a region an area with garden plots.
This made me waste at least 10 minutes.
I guess mistakes can happen, I am a bit sad though, my English is
fairly good and I really dislike finding myself misunderstanding something.
This has been a common theme in a few puzzles, I really need to work on this
and take a few minutes more to make sure my assumptions are correct,
rather than assuming I understood everything and go fast.

I was also making an error in how perimeters are counted, because I was
adding 1 to the perimeter only if the next cell is a different plant/garden plot,
but luckily I realized that before my first compilation attempt.

My only compilation failure was due to me checking if next_row > 0 and next_col > 0
instead of using >=, so the first column and row were never checked.
By adding a simpler input and with some print debugging it was clear
the problem was with perimeter calculations since the number for area
was correct, I quickly saw what was wrong.

I don't like the repetition in my "pathfinding" function, but it works.
Also "pathfinding" is not what the method is doing at all but I'm so used
to call it that way...how do you call it? Region traversal?
I'll rename it to something else before commit.
"""

answer_sample = part1("./sample_input_1.txt")
expected = 4*10 + 4*8 + 4*10 + 1*4 + 3*8 # 140
print("Answer part 1 (sample 1):", answer_sample)
assert(answer_sample == expected)

answer_sample = part1("./sample_input_3.txt")
print("Answer part 1 (sample 3):", answer_sample)
assert(answer_sample == 1930)

answer = part1("./input.txt")
print("Answer part 1:", answer)
assert(answer == 1473408)
