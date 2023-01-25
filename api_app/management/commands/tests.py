import pytest
from .bot import formula


def test_formula():
    day = 2
    assert formula(day) == 5
