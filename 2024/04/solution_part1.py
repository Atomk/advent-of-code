file = open("./input.txt")
lines = file.readlines()
file.close()

LINES_COUNT = len(lines)
LINE_LENGTH = len(lines[0])

def countXmasFromCoords(r, c) -> int:
    count = 0

    # up
    if r - 3 >= 0:
        if lines[r-1][c] == "M" and lines[r-2][c] == "A" and lines[r-3][c] == "S":
            count += 1
    # down
    if r + 3 < LINES_COUNT:
        if lines[r+1][c] == "M" and lines[r+2][c] == "A" and lines[r+3][c] == "S":
            count += 1

    # right
    if c + 3 < LINE_LENGTH:
        if lines[r][c+1] == "M" and lines[r][c+2] == "A" and lines[r][c+3] == "S":
            count += 1
    # left
    if c - 3 >= 0:
        if lines[r][c-1] == "M" and lines[r][c-2] == "A" and lines[r][c-3] == "S":
            count += 1

    # downright
    if r + 3 < LINES_COUNT and c + 3 < LINE_LENGTH:
        if lines[r+1][c+1] == "M" and lines[r+2][c+2] == "A" and lines[r+3][c+3] == "S":
            count += 1
    # downleft
    if r + 3 < LINES_COUNT and c - 3 >= 0:
        if lines[r+1][c-1] == "M" and lines[r+2][c-2] == "A" and lines[r+3][c-3] == "S":
           count += 1

    # upright
    if r - 3 >= 0 and c + 3 < LINE_LENGTH:
        if lines[r-1][c+1] == "M" and lines[r-2][c+2] == "A" and lines[r-3][c+3] == "S":
           count += 1
    # upleft
    if r - 3 >= 0 and c - 3 >= 0:
        if lines[r-1][c-1] == "M" and lines[r-2][c-2] == "A" and lines[r-3][c-3] == "S":
           count += 1

    return count

xmas_count = 0

for row in range(LINES_COUNT):
    for col in range(LINE_LENGTH):
        if lines[row][col] == "X":
            xmas_count += countXmasFromCoords(row, col)

print(xmas_count)
# assert(xmas_count == 18)      # sample_input.txt
# assert(xmas_count == 2718)    # input.txt

"""
This took me 50 minutes... Easy puzzle, just a bit tedious writing all cases and I made a couple of silly mistakes.

Is there even a better way to solve this?
For horizontal and vertical I guess you can activate some flag and look for "XMAS" or "SAMX",
but having to check diagonals made me think this approach is better.

I also thought that since the input is basically a NxM matrix, you could read all file as a single string,
remove all newlines, and use my same approach but using a single index instead of two,
but it sounds clever just for sake of being clever with dubious performance benefits.
Unless you can load all that in cache as a single array, that I guess would improve things a bit.

The silly mistakes:
I was used to working with [x][y] and then when testing against sample data I obviously had an error
and realized that "lines" stores data [y][x], the opposite, because it's an array of rows.
So I had to change that.
Then I forgot I put a "break" in the loop iterating through rows because I wanted
to test something when I first wrote rhe loop but, then forgot about it
and I thought I messed up some checks in the countXmasFromCoords() function...

I'm a bit scared for part two, I hope it's not something like day 2 where you
have to account for spelling errors. That would be annoying.
"""
