"""
Explanation was a bit tricky (especially the "antenna can also be an antinode"
but I got it, I have some ideas but also some doubts, I'll start simple
by adding all antennas to a set of locations and go from there
"""

from collections import namedtuple
from dataclasses import dataclass

Pos = namedtuple("Pos", "row col")

@dataclass
class Antenna:
    row: int
    col: int
    is_antinode: bool

def part1(data_file_path) -> int:
    file = open(data_file_path)
    antennas: dict[str, list[Antenna]] = dict()
    grid = []
    row = 0
    for line in file:
        # Must be a list so it can be edited
        grid.append(list(line.strip()))
        col = 0
        for c in grid[row]:
            if c != ".":
                if c not in antennas:
                    antennas[c] = []
                antennas[c].append(Antenna(row, col, False))
            col += 1
        row += 1
    file.close()

    height = len(grid)
    width = len(grid[0])

    antinodes_count = 0
    for freq, locations in antennas.items():
        if len(locations) == 1:
            continue
        # Compare the current antenna (A) with all other of the same type (B)
        # and check the antinode that goes in that direction (A -> B)
        for antennaA in locations:
            for antennaB in locations:
                if antennaA == antennaB:
                    continue
                r = antennaB.row - antennaA.row
                c = antennaB.col - antennaA.col
                distanceAtoB = Pos(r, c)
                antinode_pos = Pos(antennaB.row + distanceAtoB.row, antennaB.col + distanceAtoB.col)
                if 0 <= antinode_pos.row < height and 0 <= antinode_pos.col < width:
                    antinode_tile = grid[antinode_pos.row][antinode_pos.col]
                    if antinode_tile == ".":
                        grid[antinode_pos.row][antinode_pos.col] = "#"
                        antinodes_count += 1
                    elif antinode_tile != "#":
                        for antenna in antennas[antinode_tile]:
                            if antenna.row == antinode_pos.row and antenna.col == antinode_pos.col:
                                if not antenna.is_antinode:
                                    antenna.is_antinode = True
                                    antinodes_count += 1
    return antinodes_count

"""
Yeahhh first try! Did it in 35 minutes.
Used a few minuts to decide on data types and refactor to use Antenna/Pos.
The first time the code compiled, it returned the correct result.
My two compilation error were both on grid import and easy to spot:
- Wrote `grid[row] = line.strip()` instead of appending the value
  (forgot Python is not JS, new elements are not created automatically)
- Had to make grid rows lists instead of keeping them as strings because
  I needed to mutate some tiles and strings are immutable

Overall I'm satisfied with my solution, maybe I'd trade some performance
to make the "antinode count" a separate pass just to make things cleaner.
(count all "#" in the grid and then all antennas with `is_antinode == True`)
I also though of storing the antinodes in a list instead of mutating the grid
but I think what I did is simpler.
"""

print("Answer part 1 (sample):", part1("./sample_input.txt"))
assert(part1("./sample_input.txt") == 14)
print("Answer part 1:", part1("./input.txt"))
assert(part1("./input.txt") == 305)


# ------------------------------
# ----------  Part 2  ----------
# ------------------------------


"""
The way I structured my solution for the first part
should make this pretty easy, I think I can solve this
with just a couple modifications, let's see.
"""

def part2(data_file_path) -> int:
    file = open(data_file_path)
    antennas: dict[str, list[Antenna]] = dict()
    grid = []
    row = 0
    for line in file:
        # Must be a list so it can be edited
        grid.append(list(line.strip()))
        col = 0
        for c in grid[row]:
            if c != ".":
                if c not in antennas:
                    antennas[c] = []
                antennas[c].append(Antenna(row, col, False))
            col += 1
        row += 1
    file.close()

    height = len(grid)
    width = len(grid[0])

    antinodes_count = 0
    for freq, locations in antennas.items():
        if len(locations) == 1:
            continue
        # Compare the current antenna (A) with all other of the same type (B)
        # and check the antinode that goes in that direction (A -> B)
        for antennaA in locations:
            for antennaB in locations:
                if antennaA == antennaB:
                    continue
                c = antennaB.col - antennaA.col
                r = antennaB.row - antennaA.row
                distanceAtoB = Pos(r, c)
                # Antennas that have more than 1 locations also count as antinodes
                antinode_pos = Pos(antennaB.row, antennaB.col)
                while 0 <= antinode_pos.row < height and 0 <= antinode_pos.col < width:
                    antinode_tile = grid[antinode_pos.row][antinode_pos.col]
                    if antinode_tile == ".":
                        grid[antinode_pos.row][antinode_pos.col] = "#"
                        antinodes_count += 1
                    elif antinode_tile != "#":
                        for antenna in antennas[antinode_tile]:
                            if antenna.row == antinode_pos.row and antenna.col == antinode_pos.col:
                                if not antenna.is_antinode:
                                    antenna.is_antinode = True
                                    antinodes_count += 1
                    # Go to next location in the same direction
                    antinode_pos = Pos(antinode_pos.row + distanceAtoB.row, antinode_pos.col + distanceAtoB.col)
    return antinodes_count

"""
Did it first try (first compilation/execution) in 9:30 minutes!
Now we're talking. Not sure how much of this is by chance,
maybe the puzzle was easier compared to others or there were
less traps in the description or I happened to be used to structure code
in the way the puzzle required it, or maybe I am improving
and I did not miss any detail in the description,
I certainly can say I felt that two things helped:
- Even though I did not copy anything for the first part,
  loading a grid was required a few times in these puzzles and
  practice really makes me feel confident and think "oh I know how to do this".
  Same goes for named tuples and other little Python features.
  I underestimated how regular practice makes a ton of difference,
  the more I do these puzzles the less time I spend thinking about Python
  and more on the actual problem
- Similar to the first point, some puzzles had similar mechanics
  so having recently practiced similar problems it becomes
  easier to imagine what the solution may look like,
  what patterns are useful and what's a bad idea

This was Sunday's puzzle but did not have time to do it yesterday
(also due to day 6 and 7 haunting me in my dreams), now I'll get
to today's puzzle ha hopefully get back on track.
"""

print("Answer part 2 (sample):", part2("./sample_input.txt"))
assert(part2("./sample_input.txt") == 34)
print("Answer part 2:", part2("./input.txt"))
assert(part2("./input.txt") == 1150)
