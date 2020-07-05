import numpy
import sympy
from matplotlib import pyplot

from mathsnuggets.core import fields, form


class Triangle(form.Form):
    """Draw a triangle"""

    template = """
        Vertices labels: `A`, `B`, `C`<br>
        Lengths: `a`, `b`, `c`<br>
        Angles: `alpha`, `beta`, `gamma`<br>
    """

    A = fields.Field("A", default="A")
    B = fields.Field("B", default="B")
    C = fields.Field("C", default="C")

    a = fields.Expression("a")
    b = fields.Expression("b")
    c = fields.Expression("c")

    alpha = fields.Expression("alpha")
    beta = fields.Expression("beta")
    gamma = fields.Expression("gamma")

    @fields.computed("Triangle", field=fields.Html)
    @fields.figure
    def triangle(self):
        # Prepare figure
        pyplot.axis("off")
        pyplot.grid(b=None)
        pyplot.gca().set_aspect("equal")
        # Draw triangle
        x, y = zip(*(self.vertices + [numpy.array([0, 0])]))
        pyplot.plot(x, y)
        # Labelling
        m = numpy.sum(self.vertices, axis=0) / 3
        edges = zip(self.vertices, self.vertices[1:] + self.vertices[:1])
        positions = self.vertices + [numpy.sum(e, axis=0) / 2 for e in edges]
        labels = [getattr(self, attr) for attr in ["A", "B", "C", "a", "b", "c"]]
        for label, position in zip(labels, positions):
            if label:
                direction = (position - m) / numpy.linalg.norm(position - m)
                pyplot.text(*(position + 0.3 * direction), label, fontsize=13)

    @property
    def vertices(self):
        lengths = [self.a, self.b, self.c]
        angles = [self.alpha, self.beta, self.gamma]
        missing_quantities = (lengths + angles).count(None)

        def cosine_law(lengths, angles, index):
            (c, a, b), gamma = lengths[index:] + lengths[:index], angles[index]
            x, find_angle = sympy.Dummy("x"), not bool(gamma)
            gamma, c = gamma or x, c or x
            equation = sympy.Eq(c ** 2, a ** 2 + b ** 2 - 2 * a * b * sympy.cos(gamma))
            domain = sympy.Interval.open(0, sympy.pi if find_angle else sympy.oo)
            sol = [x for x in sympy.solve(equation) if x in domain][0]
            locals()["angles" if find_angle else "lengths"][index] = sol

        def sine_law(lengths, angles, i, j):
            a, b, alpha, beta = lengths[i], lengths[j], angles[i], angles[j]
            x, find_angle = sympy.Dummy("x"), not bool(beta)
            b, beta = b or x, beta or x
            equation = sympy.Eq(sympy.sin(alpha) / a, sympy.sin(beta) / b)
            # TODO: ambiguity with sine law
            domain = sympy.Interval.open(0, sympy.pi / 2 if find_angle else sympy.oo)
            sol = [x for x in sympy.solve(equation) if x in domain][0]
            locals()["angles" if find_angle else "lengths"][j] = sol

        while missing_quantities:
            missing_info = [[lengths[i], angles[i]].count(None) for i in range(3)]
            if angles.count(None) == 1:
                angles[angles.index(None)] = sympy.pi - sum([a for a in angles if a])
            elif lengths.count(None) == 0 and angles.count(None):
                cosine_law(lengths, angles, angles.index(None))
            elif lengths.count(None) == 1 and angles[lengths.index(None)]:
                cosine_law(lengths, angles, lengths.index(None))
            elif {0, 1} <= set(missing_info):
                sine_law(lengths, angles, missing_info.index(0), missing_info.index(1))
            else:
                raise ValueError("Not enough information to find the vertices")
            missing_quantities -= 1

        return [
            numpy.array([0, 0]),
            numpy.array([lengths[0].evalf(), 0], dtype=numpy.float64),
            numpy.array(
                [
                    (lengths[2] * sympy.cos(angles[1])).evalf(),
                    (lengths[2] * sympy.sin(angles[1])).evalf(),
                ],
                dtype=numpy.float64,
            ),
        ]
