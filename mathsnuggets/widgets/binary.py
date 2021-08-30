from mathsnuggets.core import fields, form


class Binary(form.MarkedForm):
    """Binary conversion"""

    answer = fields.Expression("Your answer", nosave=True, editable=True)
    expression = fields.Expression("Expression", required=True)
    convert_to = fields.Select(
        "Convert to", options=["binary", "decimal"], default="binary", required=True
    )

    template = """
        Convert `expression` to `convert_to`
        <survey
            :correct="computed.correct"
            :value="payload.answer">
            `answer`
        </survey>
    """

    @fields.computed("Correct", field=fields.Boolean)
    def correct(self):
        if not self.answer:
            return False
        if self.convert_to == "binary":
            return self.answer == int(bin(self.expression)[2:])
        else:
            return self.answer == int(self._expression, 2)


def test_binary():
    assert Binary(expression="8", convert_to="binary", answer="1000").correct
    assert Binary(expression="1000", convert_to="decimal", answer="8").correct
