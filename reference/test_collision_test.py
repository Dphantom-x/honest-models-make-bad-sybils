"""The reference statistics reproduce the numbers printed in the paper (run: python -m pytest -q)."""
import math

from collision_test import collision_evidence, coverage_evidence, log10_avoid


def split(accounts, q):
    return [range(i * q, (i + 1) * q) for i in range(accounts)]


def test_last_clean_account_of_24_is_1_in_276():
    assert math.isclose(log10_avoid(24, 22, 2), math.log10(1 / 276), rel_tol=1e-9)


def test_figure_1_endpoints():
    assert round(collision_evidence(split(12, 2), 24)[2], 2) == 9.11      # "1 in a billion"
    assert round(collision_evidence(split(12, 2), 40)[2], 2) == 3.73      # "1 in 5,321"
    assert round(collision_evidence(split(10, 3), 30)[2], 2) == 11.44


def test_shared_decoy_breaks_the_greedy_family_but_not_coverage():
    decoy = [set(s) | {0} for s in split(12, 2)]
    kept, _, e = collision_evidence(decoy, 24)
    assert kept == 1 and e == 0.0
    assert coverage_evidence([len(s) for s in decoy], 24, 24) > 2.0


def test_coverage_matches_collision_for_a_perfect_split():
    assert round(coverage_evidence([2] * 12, 24, 24), 2) == 9.11
