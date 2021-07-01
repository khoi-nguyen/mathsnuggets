from mathsnuggets.core import fields, form


class EulerMethod(form.Form):
    """Euler method"""

    template = """
        <ul>
            <li><span class="katex">f(x, y) =</span> `function`</li>
            <li>Initial condition: `x0`, `y0`</li>
            <li><span class="katex">h = </span> `h`</li>
            <li><span class="katex">n = </span> `n`</li>
            <li v-if="config.edit">`midpoint`</li>
        </ul>
        `solution`
    """

    function = fields.Expression("Function", required=True)
    x0 = fields.Expression("Initial condition (x)", required=True)
    y0 = fields.Expression("Initial condition (y)", required=True)
    h = fields.Expression("Step length", default="0.1")
    n = fields.Expression("Number of iterations", default="3")
    midpoint = fields.Boolean("Use midpoint method")

    @fields.computed("Solution")
    def solution(self):
        x, y, old_y = self.x0, self.y0, self.y0
        for k in range(self.n):
            grad = self.function.subs({"x": x, "y": y})
            if self.midpoint and k > 0:
                new_y = old_y + grad * 2 * self.h
                old_y, y = y, new_y
            else:
                y += grad * self.h
            x += self.h
        return (x.evalf(), y.evalf())
