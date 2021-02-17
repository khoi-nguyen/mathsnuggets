import sympy

from mathsnuggets.core import fields, form


class Taylor(form.Form):
    """Taylor Expansion"""

    template = """
        Taylor expansion of `expression`
        of order `order`
        <span v-if="config.edit || payload.x != 'x'">
            with respect to `x`
        </span>
        around `x0`
        `taylor`
    """

    expression = fields.Expression("Expression")
    x = fields.Expression("x", default="x")
    order = fields.Expression("Order", default=6)
    x0 = fields.Expression("x0", default=0)

    @fields.computed("Taylor expansion")
    def taylor(self):
        return sympy.series(self.expression, x=self.x, x0=self.x0, n=self.order)
