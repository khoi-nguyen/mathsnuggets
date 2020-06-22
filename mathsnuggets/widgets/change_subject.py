import sympy

from mathsnuggets.core import fields, form


class ChangeSubject(form.Form):
    """Change the subject"""

    template = "Make `variable` the subject for `equation` `solution`"

    equation = fields.Equation("Equation", required=True)
    variable = fields.Expression("Solve for", default="x", required=True)

    @fields.computed("Solution")
    def solution(self):
        solution = sympy.solve(self.equation, self.variable)
        if not solution:
            raise ValueError("The 'variable' you have entered is not in the equation")
        return sympy.Eq(
            self.variable, sympy.solveset(self.equation, self.variable).args[0]
        )
