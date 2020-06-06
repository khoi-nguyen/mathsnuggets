import sympy

from mathsnuggets.core import fields, form


class Tangent(form.Form):
    """Tangent"""

    template = """
        Find the tangent of `function` at `x` = `a` `tangent`
    """

    function = fields.Expression("Function")
    x = fields.Expression("x", default="x")
    a = fields.Expression("a")

    @fields.computed("Tangent")
    def tangent(self):
        gradient = sympy.diff(self.function, self.x).subs(self.x, self.a)
        return gradient * (self.x - self.a) + self.function.subs(self.x, self.a)
