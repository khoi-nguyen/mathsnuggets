from mathsnuggets.core import fields, form


class FractionOperations(form.Form):
    """Fractions"""

    template = "Calculate `fraction_1` `operation` `fraction_2` `solution`"

    fraction_1 = fields.Expression("fraction 1")
    fraction_2 = fields.Expression("fraction 2")
    operation = fields.Select("operation", options=["+", "-", "×", "÷"])

    @fields.computed("Solution")
    def solution(self):
        if self.operation == "+":
            answer = self.fraction_1 + self.fraction_2
        elif self.operation == "-":
            answer = self.fraction_1 - self.fraction_2
        elif self.operation == "×":
            answer = self.fraction_1 * self.fraction_2
        else:
            answer = self.fraction_1 / self.fraction_2
        return answer
