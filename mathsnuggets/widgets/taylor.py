import sympy

from mathsnuggets.core import fields, form
from mathsnuggets.widgets import plot


class Taylor(form.Form):
    """Taylor Expansion"""

    template = """
        Taylor expansion of `expression`
        of order `order`
        <span v-if="config.edit || payload.x != 'x'">
            with respect to `x`
        </span>
        around `x0`.
        <p v-if="config.edit">
            `show_graph`
            Distance to `x0`: `h`
        </p>
        `taylor`
        <div v-if="payload.show_graph">`graph`</div>
    """

    expression = fields.Expression("Expression")
    x = fields.Expression("x", default="x")
    order = fields.Expression("Order", default=6)
    x0 = fields.Expression("x0", default=0)
    show_graph = fields.Boolean("Show graph", default=False)
    h = fields.Expression("h", default="1")

    @fields.computed("Taylor expansion")
    def taylor(self):
        return sympy.series(self.expression, x=self.x, x0=self.x0, n=self.order + 1)

    @fields.computed("Plot", field=fields.Html, nohide=True)
    def graph(self):
        return plot.Plot(
            functions=[self.expression, self.taylor.removeO()],
            x=self.x,
            x_min=self.x0 - self.h,
            x_max=self.x0 + self.h,
        ).plot
