"""
The puzzle description sounds amazing! This will be fun.
Again I have two ideas,
the performant one (calculate only using the position of obstacles)
and the "bruteforce" one (visit every single tile in the map).
let's see if I can implement the first idea in a reasonable
amount of time, since it's really late here.
(I paused the timer while writing this, which I did
after reading puzzle description and before coding anything)
"""

def part1(data_file_path):
    file = open(data_file_path)

    start_row = -1
    start_col = -1
    grid = []

    row = 0
    for line in file:
        grid.append(list(line.strip()))
        if start_row == -1:
            col = 0
            for c in line:
                if c == "^":
                    start_row = row
                    start_col = col

                col += 1

        row += 1

    file.close()

    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3
    direction = UP

    # "Including the guard's starting position"
    grid[start_row][start_col] = "X"
    distinct_tiles = 1

    height = len(grid)
    width = len(grid[0])
    row = start_row
    col = start_col
    while True:
        if grid[row][col] == ".":
            grid[row][col] = "X"
            distinct_tiles += 1

        if direction == UP:
            if row - 1 < 0: break
            if grid[row-1][col] == "#":
                direction = (direction + 1) % 4
            else:
                row -= 1
        elif direction == DOWN:
            if row + 1 >= height: break
            if grid[row+1][col] == "#":
                direction = (direction + 1) % 4
            else:
                row += 1
        elif direction == LEFT:
            if col - 1 < 0: break
            if grid[row][col-1] == "#":
                direction = (direction + 1) % 4
            else:
                col -= 1
        elif direction == RIGHT:
            if col + 1 >= width: break
            if grid[row][col+1] == "#":
                direction = (direction + 1) % 4
            else:
                col += 1

    return distinct_tiles

"""
Halfway through my attempt at coding the "performant" idea,
I realized it cannot work because I have to track DISTINCT walked locations,
so I need to keep track of all walked tiles, which I thought I could avoid.
I guess the simple idea was the best idea, again.
Just make it work even if it's expensive because there's no other way,
you can just make that more efficient.
(paused timer while writing this)
"""

"""
I wasted some time with some python bullshit (I did not know
you cannot use constants in match statements, I was really confused for a bit)
Also wasted some time due to me forgetting somw quirks about python, these last days
I switched a lot between python/java/C# and I'n not the most proficient right now.
My second actual mistake was that I made the direction change when on the obstacle tile,
not before. I also recognize I have a bit of a problem with premature optiimzation,
I want to do things the most efficient way possible at first try, which does not sound
too bad of an idea but in the pursuit of efficiency I miss some implementation details
that make me waste some time, which is unfortunate since here we also care about
getting the right answer as fast as possible.
---
Final mistake, I pre-emptively applied some DRY thinking it was a good idea but no,
it ended up biting my ass. I tried to look for "#" only once per loop by using
two variables next_row and next_col, which sounded like a good idea but
they had to be updated in some unintuitive way (discovered after some debugging)
and I felt I wanted something easier to understand, so I de-DRY's all that stuff.

In the end it took me a bit more than an hour to get it right
and complete this first part of the puzzle, I feel a bit sad
but I feel I gained valuable insight in my programming habits.
---
PS.: okay I wanted to revisit that idea fot a moment and
it was actually a decent idea, but in that moment it was not obvious
to me why the two variables had to be reset at the start of each cycle
(I set them just before entering the loop and thought that was enough)
The reason is, when checking for direction I update only one of those,
so the other keeps the old value, resulting in a fail to calculate
the next tile relative to the *current* position.

Hindsight is 20/20, I gave up just before the finish line.
And also it's past 3 AM, a nice excuse for a sloppy performance.
Here's the fixed (and working!) version of my DRY idea:

while True:
    if grid[row][col] == ".":
        grid[row][col] = "X"
        distinct_tiles += 1

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
    else:
        row = next_row
        col = next_col
"""

print("Answer 1:", part1("./sample_input.txt"))
print("Answer 1:", part1("./input.txt"))
assert(part1("./sample_input.txt") == 41)
assert(part1("./input.txt") == 4580)
