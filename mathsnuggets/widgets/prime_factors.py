import sympy

from mathsnuggets.core import fields, form, tools


def is_prime_decomposition(expr):
    numbers = sympy.core.numbers
    if expr.func == sympy.Mul:
        return not False in [is_prime_decomposition(a) for a in expr.args]
    elif expr.func == sympy.Pow:
        return sympy.isprime(expr.args[0]) and expr.args[1].func in [numbers.Integer, numbers.One]
    elif expr.func in [numbers.Integer]:
        return sympy.isprime(expr)
    return False


class PrimeFactors(form.MarkedForm):
    """Prime factor decomposition"""

    answer = fields.Expression("Your answer", nosave=True, editable=True)
    integer = fields.Expression("Integer", required=True)

    template = """
        Write `integer` as a product of prime factors
        <survey :correct="computed.correct" :value="payload.answer">
            `answer`
        </survey>
    """

    @fields.computed("Correct", fields.Boolean)
    def correct(self):
        if self.answer is None or not is_prime_decomposition(self.answer):
            return False
        return tools.isequal(self.answer, self.integer, 0)


def test_prime_decomposition():
    assert PrimeFactors(integer="7", answer="7").correct
    assert PrimeFactors(integer="4", answer="2^2").correct
    assert PrimeFactors(integer="6", answer="2*3").correct
    assert PrimeFactors(integer="12", answer="2^2*3").correct
    assert not PrimeFactors(integer="13", answer="2^2*3").correct
    assert not PrimeFactors(integer="12", answer="3*4").correct
    assert not PrimeFactors(integer="2", answer="2^(1/2) * 2^(1/2)").correct
