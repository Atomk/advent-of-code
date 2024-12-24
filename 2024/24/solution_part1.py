"""
2024-12-24
I suspect this won't be too hard, since most people don't want
to spend Christmas' Eve at the computer. Let's see what this is about.
"""

def solution(data_file_path) -> int:
    file = open(data_file_path)
    wire_values: dict[str, bool] = dict()
    # First section: known wires
    while True:
        line = file.readline().strip()
        if line == "":
            break
        name = line[:3]
        value = True if line[5] == "1" else False
        wire_values[name] = value
    # Second section: expressions
    missing = []
    while True:
        line = file.readline().strip()
        if line == "":
            break
        parts = line.split()
        missing.append(parts)
    file.close()

    while len(missing) > 0:
        still_missing = []
        for parts in missing:
            first_input = parts[0]
            second_input = parts[2]
            operation = parts[1]    # AND, OR, XOR
            output_name = parts[4]

            if first_input in wire_values and second_input in wire_values:
                match operation:
                    case "AND": wire_values[output_name] = wire_values[first_input] and wire_values[second_input]
                    case "OR": wire_values[output_name] = wire_values[first_input] or wire_values[second_input]
                    case "XOR": wire_values[output_name] = wire_values[first_input] != wire_values[second_input]
            else:
                still_missing.append(parts)
        missing.clear()
        missing = still_missing

    i = 0
    result = 0
    while True:
        if i < 10:
            name = "z0" + str(i)
        else:
            name = "z" + str(i)
        if name not in wire_values:
            # Assumes there's every intermediate output name from z00 to the last zXX
            break
        if wire_values[name] is True:
            result += 2 ** i
        i += 1

    return result

"""
Done in 36 minutes. Way more then needed for this part of the puzzle which
wasn't that challenging, the description was really confusing at first though.
I could have used less time on parsing, I often lose some time by implementing
things on way and then realizing it's better to do them another way.
As far as I know this is completely normal even for professionals, but still.

Initially I did some of the "find unknown values" during the file parsing part,
so already calculating some outputs if possible when an expression lin eis parsed.
Since later I needed this again of course, I decided to keep this as a separate pass
in name of DRY principle. The increased complexity adn redundancy is not worth it
in this case, where it counts as premature optimization and I should nave done it
in the first place.
Also about that part, I don't like that I hardcoded positions in the list,
the best thing would have been an Expression class/namedtuple but I propritized
not using time for unnecessary refactors.

When it was time to test I had a couple of infinite-looping bugs that required
some "quick" debugging... Quick compared to other painfully long debugging sessions
done for previous puzzles, but in this case even 5 minutes just to find a minor
"oops I forgot" mistake is still a lot.
Here's the two bugs:
1. In the last loop of the program I forgot to write `i += 1`. As far as I know
   in Python there is no conventional way to have an infinite loop with a counter
   handled on the same line, a straightforward pattern in C-like languages where
   you can use a for loop without the loooping condition.
   This means in Python it's easier to to forget to increase the index in some
   cases like mine, I know because it's not the first time I make this mistake.
2. Wrote `still_missing.append(missing)` instead of `still_missing.append(parts)`,
   this wasn't so easy to spot. It could have been caused by me writing that part
    too hastly, but I think a big part could be bad variable naming, since
    I felt "missing" was the varible associated with the correct data. At a glance
    you cannot tell what "missing" and "parts" mean, and that they are associated.
    Naming things deserves its place in the proverbial 3 hardest problems in programming.
"""

answer_sample = solution("./sample_input.txt")
print("Answer (sample):", answer_sample)
assert(answer_sample == 4)

answer_sample = solution("./sample_input_2.txt")
print("Answer (sample_2):", answer_sample)
assert(answer_sample == 2024)

answer = solution("./input.txt")
print("Answer:", answer)
assert(answer == 61495910098126)
