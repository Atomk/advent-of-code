"""
2024-12-25
Yeah I'm doing this on Chrstmas because I forgot about it.
Holy crap this is intense, it feels like a part 1 and 2 combined.
A neat approach would be to have a function that takes a directional/numeric
pad (a grid) and a result as input and then outputs the instructions to
insert using the sequence with that pad. More than a neat approach,
this feels like the solution. Shortest path is probably just a simple manhattan
path. Now that I wrote this it feels easier, I paused the time as usual but
maybe I'll add 2-3 minutes to the total so that also thinking time is counted
for fairness.
"""

def find_button(pad_grid, search: str):
    r = 0
    for pad_row in pad_grid:
        c = 0
        for pad_button in pad_row:
            if pad_button == search:
                return r, c
            c += 1
        r += 1
    raise ValueError(f"Value '{search}' not found in this pad.")

# No empty space checks. See notes at the bottom of this file
def generate_instructions_bugged(pad_grid, output) -> str:
    curr_row, curr_col = find_button(pad_grid, "A")
    instructions: list[str] = []
    for char in output:
        dest_row, dest_col = find_button(pad_grid, char)
        # Left/right
        col_diff = dest_col - curr_col
        if col_diff < 0:
            instructions.extend(["<"] * abs(col_diff))
        elif col_diff > 0:
            instructions.extend([">"] * col_diff)
        # up/down
        row_diff = dest_row - curr_row
        if row_diff < 0:
            instructions.extend(["^"] * abs(row_diff))
        elif row_diff > 0:
            instructions.extend(["v"] * row_diff)
        # press button
        instructions.append("A")
        curr_row = dest_row
        curr_col = dest_col
    return "".join(instructions)

def generate_instructions(pad_grid, output) -> str:
    curr_row, curr_col = find_button(pad_grid, "A")
    instructions: list[str] = []
    horizontal = []
    vertical = []
    for char in output:
        dest_row, dest_col = find_button(pad_grid, char)
        horizontal.clear()
        vertical.clear()
        traverses_empty_space = False
        # Works because below the first checked axis is horizontal (col)
        if pad_grid[curr_row][dest_col] == " ":
            traverses_empty_space = True
        # Left/right
        col_diff = dest_col - curr_col
        if col_diff < 0:
            horizontal.extend(["<"] * abs(col_diff))
        elif col_diff > 0:
            horizontal.extend([">"] * col_diff)
        # up/down
        row_diff = dest_row - curr_row
        if row_diff < 0:
            vertical.extend(["^"] * abs(row_diff))
        elif row_diff > 0:
            vertical.extend(["v"] * row_diff)

        if not traverses_empty_space:
            instructions.extend(horizontal)
            instructions.extend(vertical)
        else:
            instructions.extend(vertical)
            instructions.extend(horizontal)
        # press button
        instructions.append("A")
        curr_row = dest_row
        curr_col = dest_col
    return "".join(instructions)

def execute_instructions(instructions, pad_grid) -> str:
    output: list[str] = []
    row, col = find_button(pad_grid, "A")
    for char in instructions:
        match char:
            case "<": col -= 1
            case ">": col += 1
            case "^": row -= 1
            case "v": row += 1
            case "A": output.append(pad_grid[row][col])
            case _: raise ValueError(f"Value '{char}' is not a valid instruction.")
    return "".join(output)

def solution(data_file_path) -> int:
    door_codes: list[str] = []
    file = open(data_file_path)
    for line in file:
        door_codes.append(line.strip())
    file.close()

    PAD_NUM = [
        ["7", "8", "9"],
        ["4", "5", "6"],
        ["1", "2", "3"],
        [" ", "0", "A"]
    ]

    PAD_DIR = [
        [" ", "^", "A"],
        ["<", "v", ">"]
    ]

    test_door_code = "029A"
    test = generate_instructions(PAD_NUM, test_door_code)
    assert(test == "<A^A>^^AvvvA" or test == "<A^A^>^AvvvA" or test == "<A^A^^>AvvvA")

    sample_expected_complexity = {
        "029A": 68 * 29,
        "980A": 60 * 980,
        "179A": 68 * 179,
        "456A": 64 * 456,
        "379A": 64 * 379,
    }

    # # 179A with sample data
    # you_write = "<v<A>>^A<vA<A>>^AAvAA<^A>A<v<A>>^AAvA^A<vA>^AA<A>A<v<A>A>^AAAvA<^A>A"
    # third_bot_writes = execute_instructions(you_write, PAD_DIR)
    # second_bot_writes = execute_instructions(third_bot_writes, PAD_DIR)
    # numpad_bot_writes = execute_instructions(second_bot_writes, PAD_NUM)
    # print(numpad_bot_writes)
    # print(second_bot_writes)
    # print(third_bot_writes)
    # print(you_write)
    # return 0

    complexities = []
    for door_code in door_codes:
        instr_numpad_bot = generate_instructions(PAD_NUM, door_code)
        instr_second_bot = generate_instructions(PAD_DIR, instr_numpad_bot)
        instr_third_bot = generate_instructions(PAD_DIR, instr_second_bot)
        complexity = len(instr_third_bot) * int(door_code[:3])
        complexities.append(complexity)

        # print(door_code)
        # print(instr_numpad_bot)
        # print(instr_second_bot)
        # print(instr_third_bot)
        # print(len(instr_third_bot), "*", int(door_code[:3]), "=", complexity)
        # print("")

        # assert(execute_instructions(instr_third_bot, PAD_DIR) == instr_second_bot)
        # assert(execute_instructions(instr_second_bot, PAD_DIR) == instr_numpad_bot)
        # assert(execute_instructions(instr_numpad_bot, PAD_NUM) == door_code)

        if door_code in sample_expected_complexity:
            assert(complexity == sample_expected_complexity[door_code])

    return sum(complexities)

"""
Just tried my first compilation attempt after writing all code,
this was ballsy but I was fairly confident since I thought I understood
the problem properly. Usually I test basic functionality like parsing
before attempting to get the puzzle's answer. Compilation failed because
it tripped an assertion I wrote based on the dirst example in the puzzle description.
---
First problem was an easy fix, I was comparing a string with a list.
Now instructions are returned as a string. Next.
---
Second problem, coordinate difference was calculated as 'curr - dest' but
it should be the 'dest - curr', otherwise all directions in the instructions
are mirrored (you get '<' instead of '>')
---
Forgot to write at which time I was before, now I'm at 1h22m and I've been
stuck here for at least 30 minutes, everything looks like it should work but
it does not. I took some time to analyze the example for door code 029A
and found almost everthing was correct, I was just doing a conversion too much
(I computed 4 different sets of instruction, instedad of just 3, but it feels
wrong to do just three, maybe I used the wrong names or misunderstood something,
but I'll say that the description is deliberately confusing in some places.)
Some print debugging later, most things look correct but the complexity
value of sample door coode 179A is wrong, because instructions length is
64 instead of the expected 68. Now that I have finally pinpointed this other bug
I'm tying to see it step by step again with the debugger to see what's wrong,
because I have no clue.
---
I could not undrstand, so I wrote a "execute_instructions" function to test my
instruction generator, and...everything is fine. I was really confused...
Luckuly the puzzle provides the final instructions for every door code in the
sample set, so I tried looking at the differences between what I did and that.
I chained my "execute" functions to get from those instructions to the final value,
and both my instructions and puzzle's instructions result in the correct door code.
What? (sounded like this - https://www.youtube.com/watch?v=iZ-Ayj-ht_I&t=107s)
Then re-reading the puzzle page for clues and drwing a picture, I find this:
"In particular, if a robot arm is ever aimed at a gap where no button is present
on the keypad, even for an instant, the robot will panic unrecoverably."
When I first read that I thought there is no way that makes a difference,
since there are always a few different wquivalent ways to reach a button
and all paths lead to the same result. I could not see how using a different path
would inluence the outcome, and I was already in a "I don't believe you" mood
because the text says "shortest path" multiple times like it needs some
special consideretion, I was fixated on "manhattan payh is always the simplest
and shortest in this case", and it is true, but...
After more digging and comparing differences in instructions generation I finally
got to the bottom of this, at 2h34m - a tiny difference in the instructions for the
first robot means the previous (second) robot has to give different instructions,
and maybe in one case two buttons are consecutive and require little movement,
in another case to button are further apart requiring a longer set of instructions.
first two steps (instructions for robot 1 and 2) have the same length in any case,
but the big difference is shown in instructions for the third robot, the one "you"
have to move directly, and the complexity value depends on the number of those instructions.
The difference happens because the path that can hover the "empty" button is results
in fewer final instructions than the path that avoids hovering it. So in the end I need
to check for that, pretty easy though, I can just use the other manhatan path which
means inverting the axes order (i.e. instead of going left then up, we go first up
and then left so we avoid the empty space on the left)
This puzzle is pretty dope, it took a while but I'm glad I have a pretty deep
understanding of it now, I'm still a bit shocked about the "butterlfy effect",
I wonder if there is some CS theory about the complexity of these kind of indirections.
The lesson could be that I should not have taken for granted that this detail about
spaces could be ignored, in my defence I really could not see how it would lead to
problems. If I implemented it that way I would have been faster but the solution
would work by chance (or by spec, fair enough), now after I fix this it will work
more intentionally.
---
5 minutes later, I have my fixed implementation and the sample inputs pass.
The puzzle answer I tried to submit is too high... Sooo.. Does this mean I completely
underestimated the puzzle (and overstimated my abilities) and I have to actually compute
ALL possible paths and see what creates the shortest combination?
https://www.youtube.com/watch?v=IxEIQQkhyeI&t=260s
(discovered this song/artist the other day, memes aside this tune is fire,
which is a rhyme and look, I'm tired,
this essay's not done and took me a while
so I'll write more code another time.
Self-esteem restored,
where my skills might / not reach my goal
instead of py / I'll use my word)
"""

answer_sample = solution("./sample_input.txt")
print("Answer (sample):", answer_sample)
assert(answer_sample == 126384)

answer = solution("./input.txt")
print("Answer:", answer)
# assert(answer == None)
