import sympy

from mathsnuggets.core import fields, form

test = {"expression": "x^2 - 5x + 6"}


class Simplify(form.Form):
    """Simplify"""

    expression = fields.Expression("Expression")
    template = "Simplify `expression` `simplify`"

    @fields.computed("Solution")
    def simplify(self):
        return sympy.simplify(self.expression)
