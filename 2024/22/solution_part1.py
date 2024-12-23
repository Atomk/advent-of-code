"""
2024-12-22
Skipped the previous days because of lack of time (friday)
and of motivation (saturday and almost today).
I'm a bit tired but let's try this one.
"""

def mix(secret, value):
    return secret ^ value

assert(mix(42, 15) == 37)

def prune(secret) -> int:
    return secret % 16777216

assert(prune(100000000) == 16113920)

def next_secret(secret) -> int:
    result = secret * 64
    secret ^= result
    secret = prune(secret)

    result = secret // 32
    secret ^= result
    secret = prune(secret)

    result = secret * 2048
    secret ^= result
    secret = prune(secret)

    return secret

assert(next_secret(123) == 15887950)
assert(next_secret(15887950) == 16495136)
assert(next_secret(16495136) == 527345)

def solution(data_file_path) -> int:
    file = open(data_file_path)
    initial_secret_numbers: list[int] = []
    for line in file:
        initial_secret_numbers.append(int(line.strip()))
    file.close()

    final_values = []
    for secret in initial_secret_numbers:
        for i in range(2000):
            secret = next_secret(secret)

        final_values.append(secret)

    return sum(final_values)

"""
This was easy and I could have solved it in like 15 minutes but
I didn't really process the "down" in "round down down to next integer"
so I thought I had to round, not floor/truncate. This was an English
hiccup on my part and a stupid waste of time.

Before that I forgot to assign the result of `prune()` to `secret`,
this mafe appreciate the design choice in Zig of not allowing
unused values, including return values from functions,
to avoid this kind of situations.

Now since this was pretty straightforward spec implementation like
day 19 (the interpreter thing) I expect the second part to be hard,
I just hope it's not stupidly hard (for me) like day 19.
"""

answer_sample = solution("./sample_input.txt")
print("Answer (sample):", answer_sample)
assert(answer_sample == 37327623)

answer = solution("./input.txt")
print("Answer:", answer)
assert(answer == 19822877190)
