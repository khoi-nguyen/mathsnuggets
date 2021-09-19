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


def test_lcm_hcf():
    lcm, hcf = "lowest common multiple", "highest common factor"
    assert LcmHcf(sought_quantity=lcm, numbers="61,24", answer="1464").correct
    assert LcmHcf(sought_quantity=hcf, numbers="12,6", answer="6").correct
