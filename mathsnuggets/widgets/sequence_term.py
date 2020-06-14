import sympy

from mathsnuggets.core import fields, form

test = {"sequence": "1, 3, 5, 7"}


class SequenceTerm(form.Form):
    """Sequences/Find Term"""

    template = "Find the `n`th term in `sequence` `term`"

    sequence = fields.Expression("Sequence", required=True)
    n = fields.Expression("n", required=True, default="n")

    @fields.computed("Term")
    def term(self):
        # variables need to be defined
        u_m, m, a, b, c = sympy.symbols("u_m m a b c")
        formula = a * m ** 2 + b * m + c
        # Creating system of equations to find a, b and c
        equations = [
            sympy.Eq(self.sequence[i], formula.subs(m, i + 1))
            for i in range(len(self.sequence))
        ]
        # solve the system for a, b and c
        replacements = sympy.solve(equations, dict=True)
        if replacements:
            replacements = replacements[0]
        else:
            raise ValueError(
                "The sequence you have entered is neither linear nor quadratic"
            )
        # replace variable m with user input
        replacements[m] = self.n
        return sympy.Eq(
            sympy.Symbol(f"u_{self.n}"), sympy.simplify(formula.subs(replacements))
        )
