import uuid

from mathsnuggets.core import fields, form


class Survey(form.Form):
    """Survey"""

    name = fields.Field("Survey name")
    answer = fields.Expression("Your answer", nosave=True)
    correct_answer = fields.Expression("Correct Answer")

    template = """
        <p v-if="config.edit">Correct answer: `correct_answer`</p>
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
        return self.answer == self.correct_answer

    def validate(self):
        if not self.name:
            self.name = str(uuid.uuid1())
