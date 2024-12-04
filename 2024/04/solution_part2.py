file = open("./input.txt")
# file = open("./sample_input.txt")
lines = file.readlines()
file.close()

LINES_COUNT = len(lines)
LINE_LENGTH = len(lines[0])

def isXmasAtCoords(r, c) -> bool:
    # up
    if r == 0: return False
    # down
    if r + 1 >= LINES_COUNT: return False
    # left
    if c == 0: return False
    # right
    if c + 1 >= LINE_LENGTH: return False

    # first diagonal (\)
    if (lines[r-1][c-1] == "M" and lines[r+1][c+1] == "S") or (lines[r-1][c-1] == "S" and lines[r+1][c+1] == "M"):
        # second diagonal (/)
        if (lines[r-1][c+1] == "M" and lines[r+1][c-1] == "S") or (lines[r-1][c+1] == "S" and lines[r+1][c-1] == "M"):
            return True

    return False

xmas_count = 0

for row in range(LINES_COUNT):
    for col in range(LINE_LENGTH):
        if lines[row][col] == "A":
            if isXmasAtCoords(row, col):
                xmas_count += 1

print("Answer:", xmas_count)
# assert(xmas_count == 9)      # sample_input.txt
assert(xmas_count == 2046)    # input.txt

"""
After reading the puzzle description for this part I felt relieved, I thought to myself "easy"!
I could reuse most of what I did for the first part, and to some extent I was right,
I simplified a lot the code and after a couple hiccups I got the right answer in 17 minutes.
(ps. note that being able to reuse a lot of code from the previous part helped,
and having just practiced the similar puzzle of the first part)

I thought I could do it in like, 5-10 minutes at most, I feel slow.
It's notoriously hard to make accurate estimates,
but maybe I overestimated how much work I can squeeze in 5 minutes,
and some things just take more time than we expect.

My first mistake was that after copy-pasting I forgot a minus to a plus.
My second mistake was that after copy-pasting a check I forgot to change a "c + 3" to "c + 1",
which made the script return the answer 2029 instead of the correct one, 2046.
We could say I got the answer at second try?

Did not enjoy it as much as the previous days, as I also said for the first part
both solutions were just a bit tedious but not hard, I hoped for something a bit more interesting.
Maybe I should consider using sample data cheating and try to solve without testing against that before
submitting my answer to the website? That would force me to be a bit more careful while writing code,
it's not like I randomly throw stuff at the script until it works,
but I think I could waste less time on tiny mistake by being a bit more careful.

So far I'm writing everything from scratch without any setup,
maybe I can "cheat" a little by keeping a sort of template with print/assert
and part1()/part2() so I don't feel like I'm wasting time by rewriting those for each solution.
"""
