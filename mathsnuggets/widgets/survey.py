import uuid

import sympy

from mathsnuggets.core import fields, form


class Survey(form.Form):
    """Survey"""

    name = fields.Field("Survey name")
    answer = fields.Expression("Your answer", nosave=True, editable=True)
    correct_answer = fields.Expression("Correct Answer", required=True)
    max_error = fields.Expression("Maximal error", default=0)

    template = """
        <p v-if="config.edit">
            Correct answer: `correct_answer`
            Tolerated error: `max_error`
        </p>
        <survey
            :name="payload.name"
            :showStats="config.authState.loggedIn"
            :correct="computed.correct"
            :value="payload.answer">
            `answer`
        </survey>
    """

    @fields.computed("Correct", field=fields.Boolean)
    def correct(self):
        if self.answer is None:
            return False
        return (
            sympy.Abs(sympy.simplify(self.answer - self.correct_answer))
            <= self.max_error
        )

    def validate(self):
        if not self.name:
            self.name = str(uuid.uuid1())
