"""
Mmm this sounded pretty hard a t first but seeing the examples helps a ton.
Again there's the bruteforce way and the maybe more performant way, but
considering what happened with the first part I think I'll take a few
additional minutes to think more about what the solution may look like
then maaybe start with bruteforcing it and see if I see
some opportunities for optimizations along the way.

---

Ok I just realized two things:
- I need to decide a way to detect a loop. I think a good idea would be
  "I already encountered this obstacle coming from this direction".
- The bruteforce approach means checking the whole map width*height times,
  once for every map tile. That's pretty expensive
    - Oh, but we can just try to insert an obstacle on the path the guard actually walks on,
      so we don't need to try putting a new obstacle on EVERY tile on the map.
- In this second part we don't need to see if we already crossed a path I think.
    - But finding an already walked tile could be a good moment to create an obstacle
      and see if it makes the guard follow already walked tiles in the same direction
        - This works only if a loop can only be caused by an obstacle put near a "cross path" point
          (making it a sort of 3-way cross)
"""


from collections import namedtuple
Obstacle = namedtuple("Obstacle", ["row", "col", "encounter_direction"])
Tile = namedtuple("Tile", ["row", "col"])

UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3

def isLoop(grid, start: Tile, start_direction, new_obstacle_tile: Tile):
    obstacles_found = []
    height = len(grid)
    width = len(grid[0])
    direction = start_direction
    row = start.row
    col = start.col
    while True:
        next_row = row
        next_col = col

        if direction == UP:
            if row - 1 < 0: return False
            next_row = row - 1
        elif direction == DOWN:
            if row + 1 >= height: return False
            next_row = row + 1
        elif direction == LEFT:
            if col - 1 < 0: return False
            next_col = col - 1
        elif direction == RIGHT:
            if col + 1 >= width: return False
            next_col = col + 1

        if grid[next_row][next_col] == "#" or (next_row == new_obstacle_tile.row and next_col == new_obstacle_tile.col):
            obstacle = Obstacle(next_row, next_col, direction)
            # It's a loop if already encountered this obstacle from this direction
            for obs in obstacles_found:
                if obs == obstacle:
                    return True
            obstacles_found.append(obstacle)
            direction = (direction + 1) % 4
        else:
            row = next_row
            col = next_col


def getGridAndStartPoint(file_path):
    file = open(file_path)

    start: Tile = None
    grid = []

    row = 0
    for line in file:
        grid.append(list(line.strip()))
        if start is None:
            col = 0
            for c in line:
                if c == "^":
                    start = Tile(row, col)
                col += 1
        row += 1

    file.close()

    return grid, start


def part2(data_file_path) -> int:
    grid, start_tile = getGridAndStartPoint(data_file_path)
    direction = UP
    height = len(grid)
    width = len(grid[0])
    row = start_tile.row
    col = start_tile.col
    changed_direction = False
    successful_loops = []
    while True:
        next_row = row
        next_col = col

        if direction == UP:
            if row - 1 < 0: break
            next_row = row - 1
        elif direction == DOWN:
            if row + 1 >= height: break
            next_row = row + 1
        elif direction == LEFT:
            if col - 1 < 0: break
            next_col = col - 1
        elif direction == RIGHT:
            if col + 1 >= width: break
            next_col = col + 1

        if grid[next_row][next_col] == "#":
            direction = (direction + 1) % 4
            changed_direction = True
        else:
            # Cannot create an obstacle if guard changed direction on this tile,
            # otherwise guard may change direction two times in a row on same tile
            if not changed_direction:
                # "The new obstruction can't be placed at the guard's starting position"
                if next_row != start_tile.row or next_col != start_tile.col:
                    new_obstacle_tile = Tile(next_row, next_col)
                    if new_obstacle_tile not in successful_loops:
                        # if isLoop(grid, start_tile, UP, Tile(next_row, next_col)): #works
                        if isLoop(grid, Tile(row, col), direction, Tile(next_row, next_col)):
                            successful_loops.append(new_obstacle_tile)
            changed_direction = False
            row = next_row
            col = next_col

    return len(successful_loops)

"""
1 hour in, my solution passes the sample input test but not the other one.
Apparently the value I get is too high (1626), so my loop detection strategy
is not strict enough.
---
1h20m in, I though I found and fixed a problem (double change of direction on same tile)
but answer is still too high (1583)...
---
1443 is too low :(
What am I even doing wrong
2h10m, i give up
"""

print("Answer part 2:", part2("./sample_input.txt"))
assert(part2("./sample_input.txt") == 6)
print("Answer part 2:", part2("./input.txt"))
# assert(part2("./input.txt") == 4580)
