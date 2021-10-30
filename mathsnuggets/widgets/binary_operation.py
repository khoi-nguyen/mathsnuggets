import sympy

from mathsnuggets.core import fields, form


class BinaryOperation(form.MarkedForm):
    """Binary operations"""

    term_1 = fields.Expression("Term 1", required=True)
    term_2 = fields.Expression("Term 2", required=True)
    answer = fields.Expression("Your answer", nosave=True, editable=True)
    operation = fields.Select(
        "operation", options=["+", "-", "×", "÷"], default="+", required=True
    )

    template = """
        Calculate `term_1` `operation` `term_2` in binary
        <survey
            :correct="computed.correct"
            :value="payload.answer">
            `answer`
        </survey>
    """

    @property
    def op(self):
        operations = {
            "+": sympy.Add,
            "-": lambda a, b: a - b,
            "×": sympy.Mul,
            "÷": lambda a, b: a / b,
        }
        if self.operation:
            return operations[self.operation]

    @fields.computed("Correct", field=fields.Boolean)
    def correct(self):
        if not getattr(self, "_answer", False):
            return False
        return self.op(int(self._term_1, 2), int(self._term_2, 2)) == int(
            self._answer, 2
        )


def test_binary_operation():
    assert BinaryOperation(term_1="1", term_2="1", answer="10").correct
    assert not BinaryOperation(term_1="1", term_2="0", answer="10").correct
    assert BinaryOperation(term_1="11", term_2="11", answer="110").correct
