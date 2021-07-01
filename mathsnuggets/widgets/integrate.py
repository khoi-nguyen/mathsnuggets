import sympy

from mathsnuggets.core import fields, form

test = {"function": "sin x"}


class Integrate(form.Form):
    """Integrate"""

    template = """
        Integrate `function`
        <span v-if="config.edit || payload.x != 'x'">
            with respect to `x`
        </span>
        <span v-if="config.edit || (payload.a && payload.b)">
            between `a` and `b`
        </span>
        `integral`
    """

    function = fields.Expression("Function")
    x = fields.Expression("x", default="x")
    a = fields.Expression("a")
    b = fields.Expression("b")

    @fields.computed("Integral")
    def integral(self):
        params = self.x
        if self.a is not None and self.b is not None:
            params = (self.x, self.a, self.b)
        integral = sympy.Integral(self.function, params)
        return sympy.Eq(integral, sympy.simplify(integral.doit()))
