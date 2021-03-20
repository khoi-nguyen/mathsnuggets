import numpy
import sympy

from mathsnuggets.core import fields, form


class Simpson(form.Form):
    """Numerical integration with Simpson's method"""

    template = """
        Numerically integrate `function`
        <span v-if="config.edit || payload.x !== 'x'">
            with respect to `x`
        </span>
        between `a` and `b`
        with a half-step length of `h`.
        `integral`
    """

    function = fields.Expression("function", required=True)
    a = fields.Expression("a", numeric=True, required=True)
    b = fields.Expression("b", numeric=True, required=True)
    h = fields.Expression("h", numeric=True, required=True)
    x = fields.Expression("x", default="x", required=True)

    @property
    def n(self):
        return sympy.ceiling((self.b - self.a) / self.h)

    @fields.computed("Integral")
    def integral(self):
        f = sympy.lambdify(self.x, self.function, "numpy")
        x = numpy.linspace(self.a, self.b, self.n + 1)
        y = f(x)
        return self.h / 3 * numpy.sum(y[0:-1:2] + 4 * y[1::2] + y[2::2])

    def validate(self):
        if self.n % 2 == 1:
            raise ValueError("An even number of intervals is required")
