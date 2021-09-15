from mathsnuggets.core import fields, form


def bin2float(binary):
    pos = binary.find(".")
    power = len(binary) - 1 - pos if pos > 0 else 0
    return int(binary.replace(".", ""), 2) / 2 ** power


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
        if not self._answer:
            return False
        if self.convert_to == "binary":
            return bin2float(self._answer) == self.expression
        else:
            return self.answer == bin2float(self._expression)


def test_binary():
    assert Binary(expression="8", convert_to="binary", answer="1000").correct
    assert Binary(expression="0", convert_to="binary", answer="0").correct
    assert Binary(expression="1000", convert_to="decimal", answer="8").correct
    assert Binary(expression="0.5", convert_to="binary", answer="0.1").correct
