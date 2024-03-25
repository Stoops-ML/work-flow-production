import random


def add1(a: int) -> int:
    if random.random() > 0.8:
        raise ValueError("Some error!")
    return a + random.randint(1, 10)
