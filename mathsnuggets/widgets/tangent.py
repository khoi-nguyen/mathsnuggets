import sympy

from mathsnuggets.core import fields, form

test = {"function": "x^2", "a": "1"}


class Tangent(form.Form):
    """Tangent"""

    template = """
        Find the tangent of `function` at `x` = `a` `tangent`
    """

    function = fields.Expression("Function", required=True)
    x = fields.Expression("x", default="x")
    a = fields.Expression("a", required=True)

    @fields.computed("Tangent")
    def tangent(self):
        gradient = sympy.diff(self.function, self.x).subs(self.x, self.a)
        return gradient * (self.x - self.a) + self.function.subs(self.x, self.a)
