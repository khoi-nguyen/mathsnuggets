import re

import sympy

from mathsnuggets.core import fields, form, tools


class Survey(form.MarkedForm):
    """Marked question"""

    answer = fields.Expression("Your answer", nosave=True, editable=True)
    correct_answer = fields.Expression("Correct Answer", required=True)
    max_error = fields.Expression("Maximal error", default=0)
    before = fields.Markdown("Before field text", default="Your answer:")
    after = fields.Markdown("After field text")
    question = fields.Markdown("Question")
    marking_type = fields.Select(
        "Marking type",
        options=["Default", "Numerical", "Fraction"],
        default="Default",
    )

    template = """
        <p v-if="config.edit || payload.question">`question`</p>
        <widget-settings>
            ~correct_answer~
            ~max_error~
            ~marking_type~
        </widget-settings>
        <survey
            :correct="computed.correct"
            :value="payload.answer">
            <span v-if="config.edit || payload.before">`before`</span>
            `answer`
            <span v-if="config.edit || payload.after">`after`</span>
        </survey>
    """

    @fields.computed("Correct", field=fields.Boolean)
    def correct(self):
        if self.answer is None:
            return False
        elif self.marking_type == "Numerical":
            numbers = sympy.core.numbers
            if self.answer.func not in [
                numbers.Float,
                numbers.Integer,
                numbers.One,
                numbers.Zero,
            ]:
                return False
        elif self.marking_type == "Fraction":
            if not re.search(r"^[0-9\s/]*$", self._answer):
                return False
        return tools.isequal(self.answer, self.correct_answer, self.max_error)


def test_survey():
    assert Survey(correct_answer="1", marking_type="Numerical", answer="1").correct
    assert Survey(correct_answer="0", marking_type="Numerical", answer="0").correct
