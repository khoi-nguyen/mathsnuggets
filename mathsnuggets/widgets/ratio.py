import sympy

from mathsnuggets.core import fields
from mathsnuggets.widgets import survey

class Ratio(survey.Survey):
    """Marked question with ratio"""

    answer = fields.Ratio("Your answer", nosave=True, editable=True)
    correct_answer = fields.Ratio("Correct Answer", required=True)

    @fields.computed("Correct", field=fields.Boolean)
    def correct(self):
        if self.answer is None:
            return False
        if len(self.answer) != len(self.correct_answer):
            return False
        coefficients = {sympy.simplify(a / b) for (a, b) in zip(self.answer, self.correct_answer)}
        return len(coefficients) == 1


def test_ratio():
    assert Ratio(correct_answer="3:4:9", answer="6:8:18").correct
    assert not Ratio(correct_answer="3:4:9", answer="6:8:17").correct
    assert Ratio(correct_answer="sqrt(2):2", answer="2:sqrt(8)").correct
