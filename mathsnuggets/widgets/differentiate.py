import sympy

from mathsnuggets.core import fields, form

test = {"function": "x sin x"}


class Differentiate(form.Form):
    """Differentiate"""

    template = """
        Differentiate `function` with respect to `x` `derivative`
    """

    function = fields.Expression("function")
    x = fields.Expression("x", default="x")

    @fields.computed("Derivative")
    def derivative(self):
        derivative = sympy.Derivative(self.function, self.x)
        return sympy.Eq(derivative, derivative.doit())
