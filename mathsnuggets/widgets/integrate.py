import sympy

from mathsnuggets.core import fields, form, tools


class Integrate(form.Form):
    """Integrate"""

    template = """
        <widget-settings>
            ~marked_question~
        </widget-settings>
        Integrate `function`
        <span v-if="config.edit || payload.x != 'x'">
            with respect to `x`
        </span>
        <span v-if="config.edit || (payload.a && payload.b)">
            between `a` and `b`
        </span>
        <span v-if="!payload.marked_question">`integral`</span>
    """

    function = fields.Expression("Function")
    answer = fields.Expression("Your answer", nosave=True, editable=True)
    x = fields.Expression("x", default="x")
    a = fields.Expression("a")
    b = fields.Expression("b")
    marked_question = fields.Boolean("Marked question")

    @property
    def has_limits(self):
        return self.a is not None and self.b is not None

    @fields.computed("Correct", field=fields.Boolean)
    def correct(self):
        if not self.answer:
            return False
        return tools.isequal(sympy.simplify(self.answer), self.integral)

    @fields.computed("Integral")
    def integral(self):
        params = (self.x, self.a, self.b) if self.has_limits else self.x
        integral = sympy.Integral(self.function, params)
        if not self.has_limits:
            integral += sympy.Symbol("c")
        return sympy.simplify(integral.doit())


def test_integral():
    assert not Integrate(function="x").correct
    assert not Integrate(function="x", answer="x^2/2").correct
    assert Integrate(function="x", answer="x^2/2 + c").correct
    assert Integrate(function="x", a="0", b="1", answer="0.5").correct
