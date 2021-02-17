import sympy

from mathsnuggets.core import fields, form

test = {"function": "x sin x"}


class Differentiate(form.Form):
    """Differentiate"""

    template = """
        Differentiate `function`
        <span v-if="config.edit || payload.n !== '1'">
            <span v-if="!config.edit && payload.n === '2'">
                twice
            </span>
            <span v-else>
            `n` times
            </span>
        </span>
        <span v-if="config.edit || payload.x != 'x'">
            with respect to `x`
        </span>
        `derivative`
    """

    function = fields.Expression("Function")
    x = fields.Expression("x", default="x")
    n = fields.Expression("n", default="1")

    @fields.computed("Derivative")
    def derivative(self):
        derivative = sympy.Derivative(self.function, self.x, self.n)
        return sympy.Eq(derivative, derivative.doit())
