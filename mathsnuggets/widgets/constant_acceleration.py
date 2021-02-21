import sympy

from mathsnuggets.core import fields, form


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
