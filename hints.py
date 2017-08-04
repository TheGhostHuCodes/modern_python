from typing import *
from collections import OrderedDict, deque, namedtuple

x = 10  # type: int
y: int = 10


def f(x: int, y: Optional[int]=None) -> int:
    if y is None:
        y = 20
    return x + y


print(f(10, 20))

z: OrderedDict = OrderedDict()


def g(x: List[int]) -> None:
    print(len(x))
    print(x[2])
    for i in x:
        print(i)
    print()


g([10, 20, 30])

heights: List[float] = [97.1, 102.5, 97.5]
person: Tuple[str, float] = ('Joey', 5 * 12 + 11)
info: Tuple[str, ...] = ('Person', 'Course', 'Python', 'Raymond')

fifo: deque = deque()

print(f'The answer is {x} today')

Point = NamedTuple('Point', [('x', int), ('y', int)])
