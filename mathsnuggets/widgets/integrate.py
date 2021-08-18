import sympy

from mathsnuggets.core import fields, form, tools


class Integrate(form.MarkedForm):
    """Integrate"""

    template = """
        <widget-settings>
            ~marked_question~
            ~function~
            ~x~
            ~a~
            ~b~
        </widget-settings>
        Calculate `integral`
        <span v-if="!payload.marked_question">`solution`</span>
        <survey
            :name="payload.name"
            :correct="computed.correct"
            v-if="payload.marked_question"
            :value="payload.answer">
            Solution(s): `answer`
        </survey>
    """

    function = fields.Expression("Function", required=True)
    answer = fields.Expression("Your answer", nosave=True, editable=True)
    x = fields.Expression("x", default="x")
    a = fields.Expression("a")
    b = fields.Expression("b")
    marked_question = fields.Boolean("Marked question")

    @property
    def has_limits(self):
        return self.a is not None and self.b is not None

    @fields.computed("Correct", field=fields.Boolean)
    def correct(self):
        if not self.answer:
            return False
        return tools.isequal(sympy.simplify(self.answer), self.solution)

    @fields.computed("Integral", nohide=True)
    def integral(self):
        params = (self.x, self.a, self.b) if self.has_limits else self.x
        return sympy.Integral(self.function, params)

    @fields.computed("Solution")
    def solution(self):
        integral = self.integral
        if not self.has_limits:
            integral += sympy.Symbol("c")
        return sympy.simplify(integral.doit())


def test_integral():
    assert not Integrate(function="x").correct
    assert not Integrate(function="x", answer="x^2/2").correct
    assert Integrate(function="x", answer="x^2/2 + c").correct
    assert Integrate(function="x", a="0", b="1", answer="0.5").correct
