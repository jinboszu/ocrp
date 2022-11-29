# Copyright (c) 2022 Bo Jin <jinbostar@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.


import statistics
import random
import time
from typing import Tuple, Dict


def leveling(x: Tuple[int, ...], s: int, t: int) -> Tuple[int, ...]:
    """
    compute the resulting state by the leveling heuristic
    :param x: current state (tuple)
    :param s: stack of the required container
    :param t: tier of the required container
    :return: resulting state (tuple)
    """

    x = list(x)
    for _ in range(x[s] - 1 - t):
        i = min([i for i in range(len(x)) if i != s], key=lambda i: x[i])
        x[i] += 1
    x[s] = t
    return tuple(x)


def f0(x: Tuple[int, ...]) -> float:
    """
    compute the expected number of relocations needed
    :param x: given state
    :return: expected number of relocations needed
    """
    if any(x):
        return statistics.mean(x[s] - 1 - t + f0(leveling(x, s, t))
                               for s in range(len(x)) for t in range(x[s]))
    else:
        return 0


def f1(x: Tuple[int, ...], mem: Dict[Tuple[int, ...], float]) -> float:
    """
    compute the expected number of relocations needed
    :param x: given state
    :param mem: cache to avoid repeated computation
    :return: expected number of relocations needed
    """
    if x in mem.keys():
        return mem[x]
    elif any(x):
        mem[x] = statistics.mean(x[s] - 1 - t + f1(leveling(x, s, t), mem)
                                 for s in range(len(x)) for t in range(x[s]))
        return mem[x]
    else:
        mem[x] = 0
        return 0


def f2(x: Tuple[int, ...], mem: Dict[Tuple[int, ...], float]) -> float:
    """
    compute the expected number of relocations needed
    :param x: given state
    :param mem: cache to avoid repeated computation
    :return: expected number of relocations needed
    """
    x = tuple(sorted(x))  # 等价的最小形式
    if x in mem.keys():
        return mem[x]
    elif any(x):
        mem[x] = statistics.mean(x[s] - 1 - t + f2(leveling(x, s, t), mem)
                                 for s in range(len(x)) for t in range(x[s]))
        return mem[x]
    else:
        mem[x] = 0
        return 0


def sampling(x: Tuple[int, ...]) -> int:
    """
    calculate the expected number of relocations needed via sampling
    :param x: given state
    :return: number of relocations needed via sampling
    """
    n_rehandles = 0
    while any(x):
        items = [(s, t) for s in range(len(x)) for t in range(x[s])]
        (s, t) = random.choice(items)
        n_rehandles += x[s] - 1 - t
        x = leveling(x, s, t)
    return n_rehandles


def estimate(x: Tuple[int, ...], sample_size: int) -> float:
    """
    estimate the expected number of relocations needed
    :param x: given state
    :return: expected number of relocations needed
    """
    return statistics.mean(sampling(x) for _ in range(sample_size))


if __name__ == '__main__':
    x = (6,) * 10

    t = time.time()
    print(f2(x, {}))
    print(time.time() - t)

    t = time.time()
    print(estimate(x, 1000))
    print(time.time() - t)
