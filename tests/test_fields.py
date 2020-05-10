import pytest
from sympy import Eq, I, Symbol, evaluate, oo, symbols

from mathsnuggets.core import fields, form


class Foo(form.Form):
    field = fields.Field("Field", desc="description")
    equation = fields.Equation("Equation")
    real = fields.RealNumber("Real number")
    markdown = fields.Markdown("Markdown")

    @fields.constraint("Contraint", default=True)
    def constraint(self):
        return self.real > 0

    @fields.computed("Computed")
    def computed_field(self):
        return self.field


test = Foo()


def test_field():
    assert test.field is None

    test.field = 5
    assert test.field == 5
    assert test.computed_field == 5
    assert Foo.field.name == "field"
    assert Foo.field.desc == "description"

    class NewField(fields.Field):
        def construct(self):
            self.constructed = True

    class NewFoo(Foo):
        new_field = NewField("New Field")

    assert NewFoo.new_field.constructed

    with pytest.raises(KeyError):

        class FooBar(Foo):
            new_field = NewField("New Field", name="name")


def test_realnumber_field():
    x_real = Symbol("x", real=True)

    test.real = "x"
    assert test.real == x_real

    test.real = "1 / (x + 1)"
    assert test.real == 1 / (x_real + 1)

    assert "error" in Foo.real.validate(oo)
    assert "error" in Foo.real.validate(I)
    assert "error" not in Foo.real.validate(5)

    with pytest.raises(AttributeError):
        test.real = False
    with pytest.raises(AttributeError):
        test.real = "/"
    with pytest.raises(AttributeError):
        test.real = I
    with pytest.raises(AttributeError):
        test.real = oo
    with pytest.raises(AttributeError):
        test.real = Symbol("x", imaginary=True)


def test_equation_field():
    x, y = symbols("x y", real=True)

    with evaluate(False):
        test.equation = "3 * x + 5 = 4"
        assert test.equation == Eq(3 * x + 5, 4)

        test.equation = "3 * x + 5"
        assert test.equation == Eq(3 * x + 5, 0)

        test.equation = 3 * x + 5
        assert test.equation == Eq(3 * x + 5, 0)

        test.equation = "2 x + 3 y = y = x + y"
        assert test.equation == (Eq(2 * x + 3 * y, y), Eq(y, x + y))

        # If evaluate=True, Eq(1 / x) is False
        test.equation = "1 / x"
        assert test.equation == Eq(1 / x, 0)

    with pytest.raises(AttributeError):
        test.equation = False
    with pytest.raises(AttributeError):
        test.equation = "3 x = **"


def test_markdown_field():
    test.markdown = "**strong**"
    assert test.markdown == "<p><strong>strong</strong></p>\n"


def test_constraints():
    test.real = 3
    assert test.constraint
    test.real = -3
    assert not test.constraint
    test.constraint = False
    assert test.constraint
