import flask

from mathsnuggets.core import fields, form


class Survey(form.Form):
    """Survey"""

    name = fields.Field("Survey name")
    answer = fields.Expression("Your answer")
    correct_answer = fields.Expression("Correct Answer")

    template = """
        <p>Your answer: `answer`</p>
        <div v-if="config.edit">
            <p>Correct answer: `correct_answer` (`name`)</p>
        </div>
    """
