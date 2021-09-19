import sympy

from mathsnuggets.core import fields, form, tools


class LcmHcf(form.MarkedForm):
    """LCM/HCF"""

    answer = fields.Expression("Your answer", nosave=True, editable=True)
    numbers = fields.NumberList("Integer", required=True)
    sought_quantity = fields.Select(
        "Sought quantity",
        options=["lowest common multiple", "highest common factor"],
        required=True,
    )

    template = """
        Find the `sought_quantity` of `numbers`
        <survey :correct="computed.correct" :value="payload.answer">
            `answer`
        </survey>
    """

    @fields.computed("Correct", field=fields.Boolean)
    def correct(self):
        if self.answer is None:
            return False
        if self.sought_quantity == "highest common factor":
            return tools.isequal(self.answer, sympy.gcd(self.numbers), 0)
        else:
            return tools.isequal(self.answer, sympy.lcm(self.numbers), 0)

    a = fields.RandomNumber("a", default="0, 4")
    b = fields.RandomNumber("b", default="0, 4")
    c = fields.RandomNumber("c", default="0, 2")
    d = fields.RandomNumber("d", default="0, 4")
    e = fields.RandomNumber("e", default="0, 4")
    f = fields.RandomNumber("f", default="0, 2")
    exercise_type = fields.RandomNumber("t", default="0, 1")

    def generator(self):
        self.sought_quantity = (
            "lowest common multiple" if self.exercise_type else "highest common factor"
        )
        self.numbers = [self.first_number, self.second_number]

    @property
    def first_number(self):
        return 2 ** self.a * 3 ** self.b * 5 ** self.c

    @property
    def second_number(self):
        return 2 ** self.d * 3 ** self.e * 5 ** self.f

    @fields.constraint("Distinct", default=True, hidden=True, protected=True)
    def distinct(self):
        return self.first_number != self.second_number

    @fields.constraint("Numbers are smaller than 1000", default=True)
    def small_enough(self):
        return self.first_number < 1000 and self.second_number < 1000

    @fields.constraint("Numbers are smaller than 100")
    def small(self):
        return self.first_number < 100 and self.second_number < 100


def test_lcm_hcf():
    lcm, hcf = "lowest common multiple", "highest common factor"
    assert LcmHcf(sought_quantity=lcm, numbers="61,24", answer="1464").correct
    assert LcmHcf(sought_quantity=hcf, numbers="12,6", answer="6").correct
