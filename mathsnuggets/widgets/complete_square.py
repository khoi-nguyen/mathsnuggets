import sympy

from mathsnuggets.core import fields, form


class CompleteSquare(form.Form):
    """Complete the square"""

    template = "Complete the square for `expression` `completed_square`"

    expression = fields.Expression("Expression", required=True)

    @fields.computed("Completed Square")
    def completed_square(self):
        a, h, k, x = sympy.symbols("a h k x")
        formula = a * (x + h) ** 2 + k
        equation = sympy.expand(formula - self.expression)
        system = [equation.coeff(*t) for t in [(x, 2), (x, 1), (x, 0)]]
        replacements = sympy.solve(system)
        if not replacements:
            raise ValueError("The 'expression' you have entered is not quadratic")
        return formula.subs(replacements[0])

    a = fields.RandomNumber("a")
    h = fields.RandomNumber("h")
    k = fields.RandomNumber("k")

    def generator(self):
        x = sympy.symbols("x")
        self.expression = sympy.expand(self.a * (x + self.h) ** 2 + self.k)

    @fields.range_constraint("a non-zero", default=True, hidden=True, protected=True)
    def a_non_zero(self):
        self.a -= {0}

    @fields.range_constraint("x^2 + ...")
    def monic(self):
        self.a = {1}
