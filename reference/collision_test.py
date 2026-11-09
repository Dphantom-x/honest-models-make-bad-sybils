"""Reference implementation of the two statistics in the paper (Section 3.4 and Section 4.5).

Both ask how surprising a set of downloads would be if the accounts were unrelated people, each
picking its shards uniformly at random from a dataset of n shards.

- Collision test: walk the accounts in the order they started, keep each account whose shards
  overlap none of the accounts already kept (the "family"), and multiply, for every kept account
  after the first, the chance that a random pick of the same size would have avoided every shard
  already taken. E = -log10 of that product ("a 1-in-10^E coincidence").

- Coverage test: for all the accounts, with set sizes s_i and union U, E = -log10 P(union >= U)
  under independent random picks, computed exactly by dynamic programming. No subset is chosen,
  so a swarm cannot break it by adding a shared "decoy" download to every account.

This file holds only the published formulas; the simulator, the agent harness and the detection
pipeline are not part of this repository.
"""
from __future__ import annotations

import math
from typing import Iterable, Sequence


def _lc(a: int, b: int) -> float:
    """log C(a, b), or -inf when the binomial is zero."""
    if b < 0 or b > a:
        return -math.inf
    return math.lgamma(a + 1) - math.lgamma(b + 1) - math.lgamma(a - b + 1)


def log10_avoid(n: int, used: int, s: int) -> float:
    """log10 P(a uniform s-subset of n shards avoids `used` given shards)."""
    if s <= 0:
        return 0.0
    if n - used < s:
        return -math.inf
    return (_lc(n - used, s) - _lc(n, s)) / math.log(10)


def collision_evidence(sets_in_order: Sequence[Iterable[int]], n: int):
    """Greedy collision-free family in start order. Returns (family size, shards covered, E)."""
    used: set[int] = set()
    kept, e = 0, 0.0
    for shards in sets_in_order:
        s = set(shards)
        if s & used:
            continue
        if kept:
            e -= log10_avoid(n, len(used), len(s))
        kept += 1
        used |= s
    return kept, len(used), e


def coverage_evidence(set_sizes: Sequence[int], n: int, union: int, cap: float = 50.0) -> float:
    """-log10 P(union of independent uniform picks of the given sizes covers >= `union` shards)."""
    dist = {0: 0.0}                                      # shards covered -> log probability
    for s in set_sizes:
        nxt: dict[int, float] = {}
        for c, lp in dist.items():
            for t in range(0, s + 1):                    # t of the s picks are new shards
                if c + t > n or s - t > c:
                    continue
                l = lp + _lc(n - c, t) + _lc(c, s - t) - _lc(n, s)
                k = c + t
                if k in nxt:
                    hi, lo = max(l, nxt[k]), min(l, nxt[k])
                    nxt[k] = hi + math.log1p(math.exp(lo - hi))
                else:
                    nxt[k] = l
        dist = nxt
    tail = [lp for c, lp in dist.items() if c >= union]
    if not tail:
        return cap
    m = max(tail)
    lp = m + math.log(sum(math.exp(x - m) for x in tail))
    return min(cap, -lp / math.log(10))


if __name__ == "__main__":
    # The endpoints of Figure 1: a clean split by 12 accounts with 2 shards each, and 10 with 3.
    split = lambda accounts, q: [range(i * q, (i + 1) * q) for i in range(accounts)]
    print("24-shard dataset, 12 x 2, all taken:  E = %.2f" % collision_evidence(split(12, 2), 24)[2])
    print("40-shard dataset, 12 x 2, 24 taken:   E = %.2f" % collision_evidence(split(12, 2), 40)[2])
    print("30-shard dataset, 10 x 3, all taken:  E = %.2f" % collision_evidence(split(10, 3), 30)[2])
    # A shared decoy: every account also re-downloads shard 0, so the greedy family keeps one account.
    decoy = [set(s) | {0} for s in split(12, 2)]
    print("shared decoy, collision test:         E = %.2f" % collision_evidence(decoy, 24)[2])
    print("shared decoy, coverage test:          E = %.2f" % coverage_evidence([len(s) for s in decoy], 24, 24))
