import pytest
import sympy

from mathsnuggets.core import fields, form


class CustomForm(form.Form):
    template = "Solve `equation`"
    equation = fields.Equation("Equation", default="x^3")
    required = fields.Field("Required field", required=True)

    def validate(self):
        if str(self.equation) != "Eq(x**2, 0)":
            raise AttributeError("Wrong equation")


form = CustomForm()


def test_default_values():
    form = CustomForm(required="Hello")
    assert form.required == "Hello"

    with sympy.evaluate(False):
        assert form.equation == sympy.Eq(sympy.Symbol("x") ** 3, 0)


def test_validate():
    form.required = "Hello"
    with pytest.raises(AttributeError):
        form._validate()

    form.equation = "x^2"
    form._validate()

    form.required = None
    with pytest.raises(AttributeError):
        form._validate()
    form.required = "Hello"


def test_export():
    form.required = "Hello"
    form.equation = "x^2"
    form._validate()
    export = dict(form._fields())
    assert len(export) == 2
