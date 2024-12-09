"""
Okay I know how to do half of this because that's the first idea
I had for the first part, but it was a bit overkill, while here
it becomes useful. I think I can also recycle the single-pass
checksum loop but let's see if it makes sense doing it that way.
"""

def part2(data_file_path) -> int:
    file = open(data_file_path)
    # NOTE strip returns a clone, not ideal for a big string
    input = file.read().strip()
    file.close()

    # Position in the list id file ID
    files = []
    # Position in the list is space after that file ID
    spaces = []

    blocks = []
    numbers_count = 0
    file_id = 0
    i = 0
    for char in input:
        amount = int(char)
        if i % 2 == 0:
            files.append(amount)
            blocks.extend([file_id] * amount)
            numbers_count += amount
        else:
            spaces.append(amount)
            blocks.extend(["."] * amount)
            file_id += 1
        i += 1

    # Not sure if needed, added just in case last file has trailing free space
    if(len(files) > len(spaces)):
        spaces.append(0)

    checksum = 0
    already_done = []
    i = 0
    last_file_id = len(files) - 1
    for file_id in range(len(files)):
        blocks_to_skip = 0
        if file_id in already_done:
            blocks_to_skip += files[file_id]
            blocks_to_skip += spaces[file_id]
        else:
            # file blocks
            for j in range(files[file_id]):
                checksum += i * file_id
                i += 1
            # space blocks for current file
            if spaces[file_id] >= files[last_file_id]:
                for j in range(files[last_file_id]):
                    checksum += i * file_id
                    i += 1
                already_done.append(file_id)
                blocks_to_skip += spaces[file_id] - files[last_file_id]
            else:
                blocks_to_skip += spaces[file_id]
        last_file_id -= 1
        i += blocks_to_skip

    return checksum

"""
Exactly 30 minutes in, I tried different strategies to make my solution
for part 1 work here, but there are problems with my attempt:
1) It's not easy to reason about
2) Moving a file towards the start of the array can create more space
    that can be occupied by other files, even though I don't think
    this is actually possible since the files that can be moved there
    were probably already skipped. But I'd prefer a solution that
    does work by design, not by chance.
---
I took a few minutes to re-read the puzzle description, now I'm at 40m,
I thought I understood correctly but I missed that each file from the last
to first needs exactly one attempt to move it in the first available space.
For some reason I thought this meant that for each space from first to last
you have one attempt to fill it, but it's really not the same thing.
Maybe I was trying to force my previous solution into the problem,
or I was a little too hopeful that the solution could be that similar?
Here we go back to comprehension blunders, I need to redo this part.
"""

print("Answer part 2 (sample):", part2("./sample_input.txt"))
assert(part2("./sample_input.txt") == 2858)
# print("Answer part 2:", part2("./input.txt"))
# assert(part2("./input.txt") == ???)
