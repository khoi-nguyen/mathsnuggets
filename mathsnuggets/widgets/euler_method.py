import sympy

from mathsnuggets.core import fields, form

class EulerMethod(form.Form):
    """Euler method"""

    template = """
        <ul>
            <li><span class="katex">f(x, y) =</span> `function`</li>
            <li>Initial condition: `x0`, `y0`</li>
            <hi><span class="katex">h = </span> `h`</li>
            <hi><span class="katex">n = </span> `n`</li>
        </ul>
        `solution`
    """

    function = fields.Expression("Function", required=True)
    x0 = fields.Expression("Initial condition (x)", required=True)
    y0 = fields.Expression("Initial condition (y)", required=True)
    h = fields.Expression("Step length", default="0.1")
    n = fields.Expression("Number of iterations", default="3")

    @fields.computed("Solution")
    def solution(self):
        x, y = self.x0, self.y0
        for k in range(self.n):
            y += self.function.subs({"x": x, "y": y}) * self.h
            x += self.h
        return (x, y)
