import sympy

from mathsnuggets.core import fields, form

test = {"expression": "x^2 - 5x + 6"}


class Factorise(form.Form):
    """Factorise"""

    expression = fields.Expression("Expression")
    template = "Factorise `expression` `factorise`"

    @fields.computed("Factorised")
    def factorise(self):
        return sympy.factor(self.expression)
