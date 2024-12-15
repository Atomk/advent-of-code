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

answer_sample = day15("./sample_input_small.txt")
print("Answer (sample small):", answer_sample)
assert(answer_sample == 2028)

answer_sample = day15("./sample_input.txt")
print("Answer (sample):", answer_sample)
assert(answer_sample == 10092)

answer = day15("./input.txt")
print("Answer:", answer)
assert(answer == 1413675)
