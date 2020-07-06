import sympy

from mathsnuggets.core import fields, form


class Indices(form.Form):
    """Indices"""

    template = "Calculate `index_1` `operation` `index_2` `solution`"

    index_1 = fields.StandardForm("index 1")
    index_2 = fields.StandardForm("index 2")
    operation = fields.Select("operation", options=["×", "÷"])

    @fields.computed("Solution", field=fields.StandardForm)
    def solution(self):
        operations = {
            "×": sympy.Mul,
            "÷": lambda a, b: a / b,
        }
        if self.operation:
            return sympy.simplify(
                operations[self.operation](self.index_1, self.index_2)
            )
