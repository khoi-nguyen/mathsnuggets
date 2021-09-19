import sympy

from mathsnuggets.core import fields, form, tools
from mathsnuggets.widgets import survey


class Set(survey.Survey):
    """Set question"""

    answer = fields.Set("Your answer", nosave=True, editable=True)
    correct_answer = fields.Set("Correct Answer", required=True)

    @fields.computed("Correct", field=fields.Boolean)
    def correct(self):
        if self.answer is None:
            return False
        return self.answer == self.correct_answer


def test_set():
    assert not Set(answer="1,2", correct_answer="1,2,3").correct
    assert Set(answer="3,1,2", correct_answer="1,2,3").correct
    assert Set(answer="1,1,2,3", correct_answer="1,2,3").correct
    assert not Set(answer="1,2,3,4", correct_answer="1,2,3").correct
