import sympy

from mathsnuggets.core import fields, form

test = {
    "equation_1": "x + 2 = y",
    "equation_2": " 2x = y",
    "variable_1": "x",
    "variable_2": "y",
}


class SimultaneousEquations(form.Form):
    """Simultaneous equations"""

    template = "Solve `equation1` and `equation2` for `x` and `y` `solution`"

    equation1 = fields.Equation("equation 1", required=True)
    equation2 = fields.Equation("equation 2", required=True)
    x = fields.Expression("variable 1", default="x", required=True)
    y = fields.Expression("variable 2", default="y", required=True)

    @fields.computed("Solution")
    def solution(self):
        eq1 = self.equation1.args[0] - self.equation1.args[1]
        eq2 = self.equation2.args[0] - self.equation2.args[1]
        eq = eq1 - eq2
        value = sympy.solve(eq, self.x)
        values = sympy.solve(eq, self.y)
        return value, values
