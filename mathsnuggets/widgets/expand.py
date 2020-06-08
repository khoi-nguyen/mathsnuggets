import sympy

from mathsnuggets.core import fields, form

test = {"expression": "(x - 2) (x + 3)"}


class Expand(form.Form):
    """Expand"""

    expression = fields.Expression("Expression")
    template = "Expand `expression` `expand`"

    @fields.computed("Expanded")
    def expand(self):
        return sympy.expand(self.expression)
