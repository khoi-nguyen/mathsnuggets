import sympy

from mathsnuggets.core import fields
from mathsnuggets.widgets import survey


def simplify_set(sympy_set):
    elements = [sympy.simplify(e) for e in sympy_set.args]
    return sympy.FiniteSet(*elements)


class Set(survey.Survey):
    """Set question"""

    answer = fields.Set("Your answer", nosave=True, editable=True)
    correct_answer = fields.Set("Correct Answer", required=True)

    @fields.computed("Correct", field=fields.Boolean)
    def correct(self):
        if self.answer is None:
            return False
        return simplify_set(self.answer) == simplify_set(self.correct_answer)


def test_set():
    assert not Set(answer="1,2", correct_answer="1,2,3").correct
    assert Set(answer="3,1,2", correct_answer="1,2,3").correct
    assert Set(answer="1,1,2,3", correct_answer="1,2,3").correct
    assert not Set(answer="1,2,3,4", correct_answer="1,2,3").correct
    assert Set(answer="1.0,2,3", correct_answer="1,2,3").correct
    assert Set(answer="1.0,2,6/2", correct_answer="1,2,3").correct
