import sympy

from mathsnuggets.core import fields, form

test = {"expression": "x^2 - 5x + 6"}


class Factorise(form.MarkedForm):
    """Factorise"""

    answer = fields.Expression("Your answer", nosave=True, editable=True)
    expression = fields.Expression("Expression")
    marked_question = fields.Boolean("Marked question", default=False)
    template = """
        <widget-settings>
            ~marked_question~
        </widget-settings>
        <div>Factorise `expression`</div>
        <div v-if="!payload.marked_question">`solution`</div>
        <survey
            :correct="computed.correct"
            :value="payload.answer" v-else>
            Your answer: `answer`
        </survey>
    """

    def validate(self):
        self.expression = sympy.expand(self.expression)
        super().validate()

    @fields.computed("Correct", field=fields.Boolean)
    def correct(self):
        if (
            not self.answer
            or sympy.simplify(self.answer - self.expression) != 0
            or self.answer.func != sympy.Mul
        ):
            return False
        for term in self.answer.args:
            if sympy.factor(term).func == sympy.Mul:
                return False
        return True

    @fields.computed("Solution")
    def solution(self):
        return sympy.factor(self.expression)

    a = fields.RandomNumber("a")
    b = fields.RandomNumber("b")
    c = fields.RandomNumber("c")
    d = fields.RandomNumber("d")

    def generator(self):
        x = sympy.symbols("x")
        self.expression = sympy.expand((self.a * x + self.b) * (self.c * x + self.d))

    @fields.range_constraint(
        "non-zero expression", default=True, hidden=True, protected=True
    )
    def nonzero(self):
        self.b -= {0}
        self.c -= {0}

    @fields.range_constraint("Quadratic", default=True)
    def quadratic(self):
        self.a -= {0}
        self.c -= {0}

    @fields.range_constraint("Linear")
    def linear(self):
        self.a = {0}
