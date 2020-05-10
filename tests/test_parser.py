import pytest
from sympy import Add, Symbol, evaluate, sqrt

from mathsnuggets.parser import parse


def test_parse():
    x = Symbol("x", real=True)

    with evaluate(False):
        assert parse("5 x + 3") == 5 * x + 3

    assert parse("sqrt x") == sqrt(x)

    assert parse("sqrt 2x") == sqrt(2 * x)

    assert parse("4 + 3") == Add(4, 3, evaluate=False)

    with pytest.raises(TypeError):
        parse({})
    with pytest.raises(ValueError):
        parse("sin (")
    with pytest.raises(ValueError):
        parse("3 *")
    with pytest.raises(ValueError):
        parse("5 =")
