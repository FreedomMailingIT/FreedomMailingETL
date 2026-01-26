"""Cycle test."""


import pytest
from app_modules.utilities import compose_hlap_filename


data = [  # tuples of day in month and expected cycle number
    (1, 2), (2, 2), (3, 2), (4, 2), (5, 2), (6, 2), (7, 2),
    (8, 1), (9, 1), (10, 1), (11, 1), (12, 1), (13, 1), (14, 1), (15, 1),
    (16, 1), (17, 1), (18, 1), (19, 1), (20, 1), (21, 1), (22, 1), (23, 1),
    (24, 2), (25, 2), (26, 2), (27, 2), (28, 2), (29, 2), (30, 2), (31, 2),
]


@pytest.mark.parametrize('day, expected', data)
def test_cycle_calc(day, expected):
    """Test that cycle number being calculated correctly."""
    cycle = int(compose_hlap_filename(day=day).split('_')[1])
    assert cycle == expected, f'Day {day} expected in cycle {expected} but got cycle {cycle}.'
