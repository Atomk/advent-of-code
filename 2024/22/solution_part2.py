"""
2024-12-22
Interesting, although confusing and a bit annoying.
I think I have an idea but at this point I'm prepared
to fail misarably,
"""

Sequence = tuple[int, int, int, int]

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

def price(number: int) -> int:
    # https://stackoverflow.com/a/5254833
    return number % 10

class Buyer:
    prices: list[int]
    changes: list[int]
    unique_sequences: set[Sequence]

    def __init__(self) -> None:
        self.prices = []
        self.changes = []
        self.unique_sequences = set()

def solution(data_file_path) -> int:
    file = open(data_file_path)
    initial_secret_numbers: list[int] = []
    for line in file:
        initial_secret_numbers.append(int(line.strip()))
    file.close()

    dict_seq_prices: dict[Sequence, int] = dict()
    buyers = []
    for initial_secret in initial_secret_numbers:
        buyer = Buyer()
        buyers.append(buyer)
        # Initial prica dows not have an associated change
        prev_price = price(initial_secret)
        secret = initial_secret
        for i in range(2000):
            secret = next_secret(secret)
            current_price = price(secret)
            buyer.prices.append(current_price)
            change = current_price - prev_price
            buyer.changes.append(change)
            prev_price = current_price

            if i - 3 < 0: continue

            # A tuple with last 4 changes
            seq: Sequence = Sequence(buyer.changes[-4:])

            # if seq not in dict_seq_prices:
            #     dict_seq_prices[seq] = current_price
            # elif seq not in buyer.unique_sequences:
            #     # Add if this is the first time this buyer has this sequence
            #     dict_seq_prices[seq] += current_price

            # Equivalent to above
            # # If this is the first time this buyer has this sequence
            if seq not in buyer.unique_sequences:
                if seq in dict_seq_prices:
                    # NEVER CALLSED
                    dict_seq_prices[seq] += current_price
                else:
                    dict_seq_prices[seq] = current_price

            buyer.unique_sequences.add(seq)

    max_val = -9999
    max_seq = None
    for key, value in dict_seq_prices.items():
        if value > max_val:
            max_val = value
            max_seq = key

    print(max_seq)
    return max_val

"""
1h47m because of an infuriating bug in "Buyer" class,
I fixed it but still it does not make any sense.
I'm overall not in a good moood today and these little mistakes
make me bothe sad and angry.

The class looked like this:

class Buyer:
    prices: list[int] = []
    changes: list[int] = []
    unique_sequences: set[Sequence] = set()

I thought, if I create a new instance by calling Buyer()
hose values will be reset to their default values...
Hell no, Python kept the old values (from the previous loop iteration)
even when creating a new instance, as if those were static fields.
This is shitty on so many levels, it's such a bad default behaviour.
Skill issue a guess, maybe I did not study Python classes deep enough,
maybe I got spoiled by C# that I used a lot this week,
but it's still so frustrating.
"""

answer_sample = solution("./sample_input_2.txt")
print("Answer (sample_2):", answer_sample)
assert(answer_sample == 23)

answer = solution("./input.txt")
print("Answer:", answer)
assert(answer == 2277)
