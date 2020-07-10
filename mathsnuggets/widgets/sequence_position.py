import pytest
import sympy

from mathsnuggets.core import fields, form
from mathsnuggets.widgets import sequence_term

test = {"element": "9", "sequence": "2n + 1"}


class SequencePosition(form.Form):
    """Position in Sequence"""

    template = "Find the position of `element` in `sequence` `position`"

    sequence = fields.Expression("Sequence", required=True)
    element = fields.Expression("term", required=True)

    @fields.computed("Find position")
    def position(self):
        # determine if sequence has attribute free_symbols and check if sequence has "n"
        if (
            hasattr(self.sequence, "free_symbols")
            and sympy.symbols("n") in self.sequence.free_symbols
        ):
            general_term = self.sequence
        # solve for the general term
        else:
            general_term = sequence_term.SequenceTerm(
                sequence=str(self.sequence)
            ).term.args[1]
        # equate element to general term
        equation = sympy.Eq(self.element, general_term)
        # solve the equation
        solution_set = sympy.solveset(equation, sympy.symbols("n"), sympy.S.Naturals0)
        # solution set is natural numbers or one element
        if solution_set == sympy.S.EmptySet:
            raise ValueError(
                "The 'term' you have entered is not in the sequence you have given"
            )
        return solution_set

    a = fields.RandomNumber("a")
    b = fields.RandomNumber("b")
    c = fields.RandomNumber("c")
    n = fields.RandomNumber("n", default="0, 50")

    def generator(self):
        n = sympy.symbols("n")
        formula = self.a * n ** 2 + self.b * n + self.c
        self.sequence = formula
        self.element = formula.subs("n", self.n)

    @fields.range_constraint("Linear")
    def linear(self):
        self.a = {0}
        self.b -= {0}

    @fields.range_constraint("Quadratic")
    def quadratic(self):
        self.a -= {0}


def test_sequence_position():
    with pytest.raises(ValueError):
        SequencePosition(sequence="1, 2, 3, 4", element="1/2").position
