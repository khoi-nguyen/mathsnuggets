import sympy

from mathsnuggets.core import fields, form
from mathsnuggets.parser import parse


class ConstantAcceleration(form.Form):
    """Constant acceleration"""

    template = """
        <ul>
            <li>Displacement: `s`</li>
            <li>Initial velocity: `u`</li>
            <li>Velocity: `v`</li>
            <li>Acceleration: `a`</li>
            <li>Time: `t`</li>
        </ul>
        `answer`
    """

    s = fields.Expression("Displacement")
    u = fields.Expression("Initial velocity")
    v = fields.Expression("Velocity")
    a = fields.Expression("Acceleration")
    t = fields.Expression("Time")

    @property
    def missing(self):
        return {x for x in ["s", "u", "v", "a", "t"] if getattr(self, x, None) is None}

    def validate(self):
        return len(self.missing) <= 1

    @fields.computed("Answer")
    def answer(self):
        equations = []
        if self.missing.issubset({"s"}):
            equations.append(self.u + self.a * self.t - self.v)
        if self.missing.issubset({"u"}):
            equations.append(self.v * self.t - 1 / 2 * self.a * self.t ** 2 - self.s)
        if self.missing.issubset({"v"}):
            equations.append(self.u * self.t + 1 / 2 * self.a * self.t ** 2 - self.s)
        if self.missing.issubset({"a"}):
            equations.append((self.u + self.v) / 2 * self.t - self.s)
        if self.missing.issubset({"t"}):
            equations.append(self.u ** 2 + 2 * self.a * self.s - self.v ** 2)
        return sympy.solve(equations)


def test_constant_acceleration():
    exercise = ConstantAcceleration(s="s", u=15, v=25, a="a", t=12)
    assert len(exercise.answer) == 1
    assert exercise.answer[0][exercise.a] == 10 / 12
    assert exercise.answer[0][exercise.s] == 240

    exercise = ConstantAcceleration(s=240, u="u", v=34, a="a", t=10)
    assert len(exercise.answer) == 1
    assert exercise.answer[0][exercise.u] == 14
    assert exercise.answer[0][exercise.a] == 2

    exercise = ConstantAcceleration(s=120, u=14, a=2, t="t")
    assert len(exercise.answer) == 2
    assert exercise.answer[0][exercise.t] == -20
    assert exercise.answer[1][exercise.t] == 6
