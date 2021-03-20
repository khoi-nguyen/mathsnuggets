import numpy as np
import sympy

from mathsnuggets.core import fields, form


class Simpson(form.Form):
    """Numerical integration with Simpson's method"""

    template = """
        Integrate `function` between `a` and `b`
        with a half-step length of `h`.
        `integral`
    """

    function = fields.Expression("function", required=True)
    a = fields.Expression("a", required=True)
    b = fields.Expression("b", required=True)
    h = fields.Expression("h", required=True)
    x = fields.Expression("x", default="x", required=True)

    @property
    def n(self):
        return sympy.ceiling((self.b - self.a) / self.h)

    @fields.computed("Integral")
    def integral(self):
        f = sympy.lambdify(self.x, self.function)
        x = np.linspace(float(self.a), float(self.b), self.n + 1)
        y = f(x)
        return self.h / 3 * np.sum(y[0:-1:2] + 4 * y[1::2] + y[2::2])

    def validate(self):
        if self.n % 2 == 1:
            raise ValueError("An even number of intervals is required")
