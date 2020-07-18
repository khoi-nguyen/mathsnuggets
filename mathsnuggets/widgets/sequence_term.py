import pytest
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

    a = fields.RandomNumber("a")
    b = fields.RandomNumber("b")
    c = fields.RandomNumber("c")

    def generator(self):
        formula = self.a * self.n ** 2 + self.b * self.n + self.c
        self.sequence = tuple([formula.subs(self.n, i) for i in range(1, 5)])

    @fields.range_constraint("Linear")
    def linear(self):
        self.a = {0}
        self.b -= {0}

    @fields.range_constraint("Quadratic")
    def quadratic(self):
        self.a -= {0}

    @fields.range_constraint("Increasing")
    def increasing(self):
        self.a = {n for n in self.a if n > 0}
        self.b = {n for n in self.b if n > 0}

    @fields.range_constraint("Decreasing")
    def decreasing(self):
        self.a = {n for n in self.a if n < 0}
        self.b = {n for n in self.b if n < 0}


def test_sequence_term():
    with pytest.raises(ValueError):
        SequenceTerm(sequence="1, 1, 1, 3").term
    pass
