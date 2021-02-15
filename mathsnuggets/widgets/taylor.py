import sympy

from mathsnuggets.core import fields, form

test = {"function": "x sin x"}


class Taylor(form.Form):
    """Taylor Expansion"""

    template = """Expand `expression``expand`"""

    expression = fields.Expression("Expression")
    x = fields.Expression("x", default="x")
    order = 6

    @fields.computed("Taylor")
    def taylor(self):
        return sympy.series(self.expression, x=self.x, x0=self.x0, n=self.order)
