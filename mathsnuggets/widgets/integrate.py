import sympy

from mathsnuggets.core import fields, form

test = {"function": "sin x"}


class Integrate(form.Form):
    """Integrate"""

    template = """
        Integrate `function` with respect to `x` `integral`
    """

    function = fields.Expression("function")
    x = fields.Expression("x", default="x")

    @fields.computed("Integral")
    def integral(self):
        integral = sympy.Integral(self.function, self.x)
        return sympy.Eq(integral, integral.doit())
