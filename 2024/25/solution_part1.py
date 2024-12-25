"""
2024-12-25
I did not think I'd have time or willingness to code on Christmas,
but here we are. This sounds fairly easy, what's the catch?
"""

def schematic_to_heights_list(schematic_lines) -> list[int]:
    height = len(schematic_lines)
    width = len(schematic_lines[0])
    list_heights = []
    # row = 0
    # col = 0
    for col in range(width):
        list_heights.append(0)
        # We ignore first and last row to calc heights
        for row in range(1, height-1):
            if schematic_lines[row][col] == "#":
                list_heights[col] += 1
    return list_heights


def solution(data_file_path) -> int:
    file = open(data_file_path)
    locks: list[list[int]] = []
    keys: list[list[int]] = []
    max_height = -1
    schematic_lines = []
    while True:
        line = file.readline()
        line_stripped = line.strip()

    # for line in file:
    #     line_stripped = line.strip()
        if line_stripped != "":
            schematic_lines.append(line_stripped)
        else:
            heights_list = schematic_to_heights_list(schematic_lines)
            if schematic_lines[0][0] == "#":
                locks.append(heights_list)
            else:
                keys.append(heights_list)
            # print("max_height:", len(schematic_lines)-2)
            if max_height == -1:
                # ignore first and last row
                max_height = len(schematic_lines) - 2
            schematic_lines.clear()
            if line == "":
                # reached EOF
                break
    file.close()

    count_fitting = 0
    for lock in locks:
        for key in keys:
            fits = True
            for i in range(len(key)):
                if lock[i] + key[i] > max_height:
                    fits = False
                    # print("not fits", lock, key)
                    break
            if fits:
                count_fitting += 1
                # print("fits", lock, key)
    return count_fitting

"""
I liked this! A different concept compared to the usual grid traversal
or number-crunching puzzles. I needed around 40 minutes for this
because I was slow while writing the parsing logic (also had to re-read
some passages of the description to make sure I understood a couple details correctly)
and then had a problem with missing data for the last schematic in the file.
Basically I used the usual "for line in file" to read the file but I used the
empty lines as checkpoints to mark the schematic data as finished, but the input files
do not have a last empty line, so the parser loop stopped on last schematic line
without executing the logic to add it to the key/lock lists.
After some searching, apparently there's no way to check if we reached EOF
without reading again, and I don't want to use an additional read/seek for every line
of the file, so I just used an infinite loop with "line = file.readline()"
since I know it returns an empty string if (and only if) EOF is reached.
That solved the problem and both tests passed.
"""

answer_sample = solution("./sample_input.txt")
print("Answer (sample):", answer_sample)
assert(answer_sample == 3)

answer = solution("./input.txt")
print("Answer:", answer)
# assert(answer == None)
