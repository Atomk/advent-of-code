"""
The tricky part here is obviously moving boxes, I'll have to think
how to do that in a reasonable way, the rest is usual
mix and match of techniques already used in previous puzzles.
"""

class Pos:
    row: int
    col: int

    def __init__(self, row, col):
        self.row = row
        self.col = col

    def add(self, other):
        self.row += other.row
        self.col += other.col

    def sub(self, other):
        self.row -= other.row
        self.col -= other.col

    def equal(self, other):
        return self.row == other.row and self.col == other.col


def day15(data_file_path) -> int:
    file = open(data_file_path)
    all = file.read()
    file.close()

    parts = all.strip().split("\n\n")
    map_lines = parts[0].strip().splitlines()
    mov_string = parts[1].strip().replace("\n", "")

    HEIGHT = len(map_lines)
    WIDTH = len(map_lines[0])

    robot_pos: Pos = None

    grid = []
    for row in range(HEIGHT):
        grid.append(list(map_lines[row]))
        # print(grid[-1])
        if robot_pos is not None:
            continue
        for col in range(WIDTH):
            if grid[row][col] == "@":
                robot_pos = Pos(row, col)

    velocity = Pos(0, 0)
    for direction_char in mov_string:
        velocity.row = 0
        velocity.col = 0
        match direction_char:
            case "^": velocity.row = -1
            case "v": velocity.row = 1
            case "<": velocity.col = -1
            case ">": velocity.col = 1

        # Early return if in front of a wall. Not really necessary,
        # the code below is a bit more complicated but can check the same thing
        next_row = robot_pos.row + velocity.row
        next_col = robot_pos.col + velocity.col
        if grid[next_row][next_col] == "#":
            continue

        # Check if there's a free tile before the robot and the next wall
        tile = Pos(robot_pos.row, robot_pos.col)
        free_tile_before_wall: Pos = None
        while True:
            tile.add(velocity)
            match grid[tile.row][tile.col]:
                case "#": break
                case "O": continue
                case ".":
                    free_tile_before_wall = Pos(tile.row, tile.col)
                    break

        if free_tile_before_wall is None:
            continue

        # Move the robot and any non-wall obstacle by one tile in the
        # selected direction. The algorithm starts from the "end" position
        # instead of robot position, because this way does not
        # require the use of temp variables and it's much simpler.
        current_tile = free_tile_before_wall
        while True:
            prev_row = current_tile.row - velocity.row
            prev_col = current_tile.col - velocity.col
            grid[current_tile.row][current_tile.col] = grid[prev_row][prev_col]
            current_tile.sub(velocity)
            if grid[prev_row][prev_col] == "@":
                grid[prev_row][prev_col] = "."
                break
        robot_pos.add(velocity)

    sum_gps_coords = 0
    for row in range(HEIGHT):
        for col in range(WIDTH):
            if grid[row][col] == "O":
                sum_gps_coords += row * 100 + col

    return sum_gps_coords

"""
Did it in almost exactly one hour.
Note that despite things being similar to old puzzles, I always wrote
things from scratch without referencing old solutions (reason: as an exercise)

There were three input files (two samples and the proper input) and
a few minutes were spent setting up those and the rest of the boilerplate.

Some notes by looking at undo history:
First thing I wrote the file load and the final coordinates count,
as they were the easiest things. I refactored things a few times,
because a bit after coding directions/velocity I came up with a better
approach and I also felt code would be simpler with a Pos class,
like the last few puzzles.

The "find direction" (after said little refactoring) and the
"find next free tile before wall" parts were easy, while surprisingly
the "move everything in the line" part stumped me for a bit. In an attempt
to simplify that part I expanded the Pos class by adding methods, used those
where necessary and used the Pos class more instead of having two separate
variables for row and col. Not really necessary but it helped simplifying some logic.
While searching for a warning (apparently you cannot annotate a method parameter
with the same type of the class it's part of) I found out you can do
operator overloading in Python, that's handy and dangerous. I tried it but soon
changed my mind, with Python being dynamically typed it feels a bit scary to have
this kind of "hidden control flow" that Zig is so adamant about avoiding.

After attempting for a while to understand and implement said movement part,
it felt harder than necessary and it was clear something was wrong in my approach,
I just couldn't wrap my head around it. So I draw a picture and then it hit me,
it's MUCH easier to do in reverse! No temp variables needed or replaced tiles.
It feels like one of those algorithms/patterns that everyone who studied DSA knows,
and I'm just not there yet. Yet, but hey, I'm practicing at least.

However, bingo! This was definitely the right approach.
The good news is, despite me taking a bit long to finish this, all three tests passed first try.
The only other time I executed the code was after implementing the file load,
to ensure the map was parsed correctly (left the print statement as a comment)

---
I'll skip the second part because it looks annoying and long and I want to do
some other things today. I'd also like to finish the second for the previous days
where I skipped it (or I made an attempt and failed, or better, stopped trying)
"""

answer_sample = day15("./sample_input_small.txt")
print("Answer (sample small):", answer_sample)
assert(answer_sample == 2028)

answer_sample = day15("./sample_input.txt")
print("Answer (sample):", answer_sample)
assert(answer_sample == 10092)

answer = day15("./input.txt")
print("Answer:", answer)
assert(answer == 1413675)
