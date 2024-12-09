"""
Take two, lets try a different approach.
"""

from dataclasses import dataclass

@dataclass
class File:
    id: int
    blocks: int
    spaces: int
    attempted_relocation: bool

def print_all_blocks(files):
    for file in files:
        for j in range(file.blocks):
            print(file.id, sep="", end="")
        for j in range(file.spaces):
            print(".", sep="", end="")
    # new line
    print()

def part2(data_file_path) -> int:
    file = open(data_file_path)
    # NOTE strip returns a clone, not ideal for a big string
    input = file.read().strip()
    file.close()

    files: list[File] = []
    file_id = 0
    i = 0
    for char in input:
        amount = int(char)
        if i % 2 == 0:
            files.append(File(file_id, amount, 0, False))
            file_id += 1
        else:
            files[-1].spaces = amount
        i += 1

    # --- relocation ---
    last_file_index = len(files) -1
    while last_file_index >= 1:
        relocation_happened = False
        last_file = files[last_file_index]
        if not last_file.attempted_relocation:
            last_file.attempted_relocation = True
            for i, file in enumerate(files):
                # Free space must be before the file to relocate
                if i >= last_file_index:
                    break
                if file.spaces >= last_file.blocks:
                    # Put spaces where the moved file came from
                    files[last_file_index - 1].spaces += last_file.blocks + last_file.spaces
                    # Change spaces at moved file destination
                    remaining_space = (file.spaces - last_file.blocks)
                    file.spaces = 0
                    last_file.spaces = remaining_space
                    # Actually move the file
                    removed = files.pop(last_file_index)
                    files.insert(i+1, removed)
                    relocation_happened = True
                    #print_all_blocks(files)
                    break

        # Keep same index if order of files was changed
        if not relocation_happened:
            last_file_index -= 1

    # --- checksum ---
    checksum = 0
    i = 0
    for file in files:
        for j in range(file.blocks):
            checksum += i * file.id
            i += 1
        i += file.spaces

    return checksum

"""
Finally, after almost one hour since the start of this new attempt, I solved this.
First thing I did was to create the File class, it looked like a good abstraction
for this problem, even though later I realized that maybe a generic "Section"
would make relocations easier since it can represent a group of block,
be it files or spaces, but I still needed to track file ID and relocation status
so I kept is that way.
In this attempt I finally separated the checksum part in its own pass,
it's really straightforward and since the relocation part is tricky some
Major time wasters were thinking how to best organize things, choose meaningful names,
The major time waster was that I forgot to limit the search of available free space
to blocks BEFORE the file to relocate, it took some print debugging and
head scratching to find out.
I also spent some time trying to organize things in a way that made sense,
choose meaningful name, write a comment here and there, it's both a blessing
and a curse but whatever I write I can't stop myself from making sure future me
can understand what's going on, even though this is mostly throwaway code
that exists just to get a number I'll most probably never need again.
Anyway we're back on track baby! I'm just missing the second star for
the evil day 6, and maybe some benchmarking on a couple solution just
out of curiosity.
"""

answer_sample = part2("./sample_input.txt")
print("Answer part 2 (sample):", answer_sample)
assert(answer_sample == 2858)

answer = part2("./input.txt")
print("Answer part 2:", answer)
assert(answer == 6511178035564)
