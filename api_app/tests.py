import pytest

from api_app.management.commands.bot import formula

day = 2


def test_formula():
    assert formula(day) == 5
