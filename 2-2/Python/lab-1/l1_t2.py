from typing import List

def angle(hours, minutes):
    hours_angel = hours * 30 + minutes * 0.5
    minutes_angel = minutes * 6
    return hours_angel - minutes_angel


print(angle(8, 40))
print(angle(10, 35))

def seq1(n: int) -> List[int]:
    sequence: List = []
    for i in range(1, n + 1):
        sequence.append(2 ** i + 1)
    return sequence


print(seq1(8))


def seq2(n: int) -> List[int]:
    sequence: List = []
    for i in range(1, n + 1):
        sequence.append(2 ** i - 1)
    return sequence


print(seq2(8))


def seq3(n: int) -> List[int]:
    sequence: List = []
    for i in range(1, n + 1):
        sequence.append((i * (i + 1)) // 2 + 1)
    return sequence


print(seq3(8))


def sum_of_digits(x: int) -> int:
    return sum(int(digit) for digit in str(x))


def seq4(n: int) -> List[int]:
    sequence: List = [2]
    for i in range(1, n):
        next_term = sum_of_digits(sequence[-1]) ** 2
        sequence.append(next_term)
    return sequence


print(seq4(8))


def seq5(n: int) -> List[int]:
    sequence: List = [1, 2]
    for i in range(2, n):
        if (i + 1) % 3 == 0:
            sequence.append((sequence[i - 1] + sequence[i - 2]) * 2)
        else:
            sequence.append(sequence[i - 1] + sequence[i - 2])
    return sequence


print(seq5(8))
