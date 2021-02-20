import numpy
import pytest
import sympy
from matplotlib import pyplot

from mathsnuggets.core import fields, form

test = {"a": "3", "b": "4", "c": "5"}


class Triangle(form.Form):
    """Draw a triangle"""

    template = """
        <div v-if="config.edit">
            Vertices labels: `A`, `B`, `C`<br>
            Lengths: `a`, `b`, `c`<br>
            Angles: `alpha`, `beta`, `gamma`<br>
        </div>
        `triangle`
    """

    A = fields.Expression("A", default="A")
    B = fields.Expression("B", default="B")
    C = fields.Expression("C", default="C")

    a = fields.Expression("a")
    b = fields.Expression("b")
    c = fields.Expression("c")

    alpha = fields.Expression("alpha")
    beta = fields.Expression("beta")
    gamma = fields.Expression("gamma")
    obtuse = fields.Field("Obtuse (sine law ambiguity)", default=False)

    @fields.computed("Triangle", field=fields.Html, nohide=True)
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
        positions = (
            self.vertices + [numpy.sum(e, axis=0) / 2 for e in edges] + self.vertices
        )
        labels = [
            getattr(self, attr)
            for attr in ["A", "B", "C", "a", "b", "c", "beta", "gamma", "alpha"]
        ]
        signs = [1 if i < 6 else -1 for i in range(9)]
        for label, position, sign in zip(labels, positions, signs):
            if label:
                label = fr"${sympy.latex(label)}$"
                direction = (position - m) / numpy.linalg.norm(position - m)
                pyplot.text(*(position + 0.3 * sign * direction), label, fontsize=13)

    @property
    def vertices(self):
        lengths = [self.a, self.b, self.c]
        angles = [self.alpha, self.beta, self.gamma]

        def missing(expressions):
            return [
                i
                for i, e in enumerate(expressions)
                if not e or getattr(e, "func", "") == sympy.Symbol
            ]

        missing_quantities = len(missing(lengths + angles))

        def cosine_law(lengths, angles, index):
            (c, a, b), gamma = lengths[index:] + lengths[:index], angles[index]
            x, find_angle = sympy.Dummy("x"), not bool(gamma)
            gamma, c = gamma or x, c or x
            equation = sympy.Eq(c ** 2, a ** 2 + b ** 2 - 2 * a * b * sympy.cos(gamma))
            domain = sympy.Interval.open(0, sympy.pi if find_angle else sympy.oo)
            sol = [x for x in sympy.solve(equation) if x in domain]
            if not sol:
                raise ValueError(
                    "The lengths and angles must satisfy the law of cosines"
                )
            locals()["angles" if find_angle else "lengths"][index] = sol[0]

        def sine_law(lengths, angles, i, j):
            a, b, alpha, beta = lengths[i], lengths[j], angles[i], angles[j]
            x, find_angle = sympy.Dummy("x"), not bool(beta)
            b, beta = b or x, beta or x
            equation = sympy.Eq(sympy.sin(alpha) / a, sympy.sin(beta) / b)
            domain = sympy.Interval.open(0, sympy.pi if find_angle else sympy.oo)
            sol = [x for x in sympy.solve(equation) if x in domain]
            if not sol:
                raise ValueError("The lengths and angles must satisfy the law of sines")
            sol = [
                x
                for x in sol
                if x + sum([a for a in angles if a and not a.free_symbols]) < sympy.pi
            ]
            sol = sol[1] if self.obtuse and len(sol) == 2 else sol[0]
            locals()["angles" if find_angle else "lengths"][j] = sol

        while missing_quantities:
            missing_info = [len(missing(el)) for el in zip(lengths, angles)]
            if len(missing(angles)) == 1:
                angle = sympy.pi - sum([a for a in angles if a and not a.free_symbols])
                if angle not in sympy.Interval.open(0, sympy.pi):
                    raise ValueError("The angles sum cannot exceed 180 degrees")
                angles[missing(angles)[0]] = angle
            elif not missing(lengths) and missing(angles):
                cosine_law(lengths, angles, missing(angles)[0])
            elif len(missing(lengths)) == 1 and missing(lengths)[0] not in missing(
                angles
            ):
                cosine_law(lengths, angles, missing(lengths)[0])
            elif {0, 1} <= set(missing_info):
                sine_law(lengths, angles, missing_info.index(0), missing_info.index(1))
            else:
                raise ValueError("Not enough information to find the vertices")
            missing_quantities -= 1

        equations = [
            sympy.Eq(
                (lengths[2] * sympy.cos(angles[1])).evalf(5),
                (lengths[0] - lengths[1] * sympy.cos(angles[2])).evalf(5),
            ),
            sympy.Eq(
                (lengths[2] * sympy.sin(angles[1])).evalf(5),
                (lengths[1] * sympy.sin(angles[2])).evalf(5),
            ),
            sympy.Eq(sum(angles).evalf(5), sympy.pi.evalf(5)),
        ]
        if not all(equations):
            raise ValueError("There are no triangles satisfying the conditions")
        # if self.obtuse and not [a for a in angles if a > sympy.pi / 2]:
        #     raise ValueError("Could not find an appropriate obtuse triangle")

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


def test_triangle():
    assert Triangle(a=3, b=4, c=5).triangle

    assert Triangle(a=3, b=4, c="c", gamma="pi/2").triangle

    with pytest.raises(ValueError):
        assert Triangle(a=3, b=4, c=5, gamma="pi").vertices

    with pytest.raises(ValueError):
        assert Triangle(a=3, b=4, c=5, gamma="pi/4").vertices

    with pytest.raises(ValueError):
        assert Triangle(a=3, b=4, c=15).vertices

    with pytest.raises(ValueError):
        assert Triangle(a=4, b=4, c=4, obtuse=True).vertices

    # Sine law: no triangle
    with pytest.raises(ValueError):
        assert Triangle(b=7, c=16, beta="pi/6").vertices

    # Ambiguous case
    triangle = Triangle(b=10, c=16, beta="pi/6")
    triangle2 = Triangle(b=10, c=16, beta="pi/6", obtuse=True)
    assert triangle.vertices[1][0] != triangle2.vertices[1][0]
