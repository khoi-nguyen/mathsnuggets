import sympy

from mathsnuggets.core import fields, form


class Pythagoras(form.Form):
    """Pythagoras"""

    template = "Find the missing length of triangle `a` `b` `c` `length`"

    a = fields.Expression("a", default="a")
    b = fields.Expression("b", default="b")
    c = fields.Expression("c", default="c")

    @fields.computed("Length")
    def length(self):
        return sympy.solve(sympy.Eq(self.a ** 2 + self.b ** 2, self.c ** 2))
