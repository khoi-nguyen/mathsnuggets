import pytest
import sympy

from mathsnuggets.core import fields, form


class Widget(form.Form):

    a = fields.RandomNumber("a")
    b = fields.RandomNumber("b")

    field = fields.Field("Field")

    @fields.constraint("Constraint")
    def constraint(self):
        return self.a == self.b

    @fields.range_constraint("Range constraint")
    def range_constraint(self):
        self.a = sympy.symbols("a b c")

    def generator(self):
        self.field = sympy.Eq(self.a, self.b, evaluate=False)


def test_random_number():
    test = Widget()
    assert isinstance(test.a, set)
    assert len(test.a) > 1

    with pytest.raises(ValueError):
        test.a = "1, 3, 5"

    test.a = 5
    assert test.a == {5}
    test.generate()
    assert test.a == 5
    test._random = {}
    assert test.a == {5}

    test.a = sympy.symbols("x y z")
    assert isinstance(test.a, set)
    test.generate()
    assert isinstance(test.a, sympy.Symbol)


def test_range_constraint():
    test = Widget()
    test.range_constraint = True
    test.generate()
    assert test.a in sympy.symbols("a b c")

    test = Widget()
    test.range_constraint = False
    test.generate()
    assert test.a not in sympy.symbols("a b c")


def test_generator():
    test = Widget()
    test.constraint = True
    test.generate()

    assert test.constraint
    assert test.a == test.b
