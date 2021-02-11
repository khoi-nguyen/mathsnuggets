import sympy

from mathsnuggets.core import fields, form

test = {"function": "x sin x"}


class Taylor(form.Form):
    """Taylor Expansion"""

    template = """
            Expand `expression``expand`
    """

    expression = fields.Expression("Expression")
    x = fields.Expression("x", default="x")

    @fields.computed("Taylor")
    def taylor(self):
        return sympy.series(self.expression)
