import pytest

from exp_bot_app.management.commands.bot import formula

day = 2


def test_formula():
    assert formula(day) == 5
