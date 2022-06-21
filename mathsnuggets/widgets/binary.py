from mathsnuggets.core import fields, form


def bin2float(binary):
    pos = binary.find(".")
    power = len(binary) - 1 - pos if pos > 0 else 0
    return int(binary.replace(".", ""), 2) / 2 ** power


class Binary(form.MarkedForm):
    """Binary conversion"""

    answer = fields.Expression("Your answer", nosave=True, editable=True)
    expression = fields.Expression("Expression", required=True)
    base = fields.Expression("Base", required=True, default="2", setting=True)

    template = """
        Convert `expression` to `convert_to`
        <survey
            :correct="computed.correct"
            :value="payload.answer">
            `answer`
        </survey>
    """
    
    @fields.computed("Convert to", field=fields.Field, nohide=True)
    def convert_to(self):
        if self.base == 2 or not self.base:
            return "binary"
        if self.base == 10:
            return "decimal"
        return f"base {self.base}"

    @fields.computed("Correct", field=fields.Boolean)
    def correct(self):
        if not getattr(self, "_answer", False):
            return False
        if self.base == 2:
            return bin2float(self._answer) == self.expression
        if self.base == 10:
            return self.answer == bin2float(self._expression)
        return int(self.answer, self.base) == self.expression


def test_binary():
    assert Binary(expression="8", convert_to="binary", answer="1000").correct
    assert Binary(expression="0", convert_to="binary", answer="0").correct
    assert Binary(expression="1000", convert_to="decimal", answer="8").correct
    assert Binary(expression="0.5", convert_to="binary", answer="0.1").correct
    assert Binary(expression="7", base="7", answer="10").correct
