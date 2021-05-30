import re
import uuid

import sympy

from mathsnuggets.core import fields, form


class Survey(form.Form):
    """Marked question"""

    name = fields.Field("Survey name")
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
        <widget-settings v-if="config.edit">
            <config-option name="Correct Answer">`correct_answer`</config-option>
            <config-option name="Tolerated error">`max_error`</config-option>
            <config-option name="Marking type">`marking_type`</config-option>
        </widget-settings>
        <survey
            :config="config"
            :name="payload.name"
            :showStats="config.authState.loggedIn"
            :correct="computed.correct"
            :value="payload.answer">
            <span v-if="config.edit || payload.before">`before`</span>
            `answer`
            <span v-if="config.edit || payload.after">`after`</span>
        </survey>
    """

    _total_marks = 1

    @property
    def _marks(self):
        return 1 if self.correct else 0

    @fields.computed("Correct", field=fields.Boolean)
    def correct(self):
        if self.answer is None:
            return False
        elif self.marking_type == "Numerical":
            numbers = sympy.core.numbers
            if not self.answer.func in [numbers.Float, numbers.Integer]:
                return False
        elif self.marking_type == "Fraction":
            if not re.search(r"^[0-9\s/]*$", self._answer):
                return False
        return (
            sympy.Abs(sympy.simplify(self.answer - self.correct_answer))
            <= self.max_error
        )

    def validate(self):
        if not self.name:
            self.name = str(uuid.uuid1())
