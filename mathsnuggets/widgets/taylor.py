import sympy

from mathsnuggets.core import fields, form

class Taylor(form.Form):
    """Taylor Expansion"""

    template = """Taylor expansion of `expression` of order `order` with respect to `x` around `x0`"""

    expression = fields.Expression("Expression")
    x = fields.Expression("x", default="x")
    order = fields.Expression("Order", default=6)

    @fields.computed("Taylor")
    def taylor(self):
        return sympy.series(self.expression, x=self.x, x0=self.x0, n=self.order)
