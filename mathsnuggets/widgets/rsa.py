import sympy

from mathsnuggets.core import fields, form

class Rsa(form.MarkedForm):
    """RSA"""

    answer = fields.Expression("Decrypted message", nosave=True, editable=True)
    m = fields.Expression("Encrypted message", required=True)
    p = fields.Expression("Prime number", required=True, setting=True)
    q = fields.Expression("Prime number", required=True, setting=True)
    m = fields.Expression("Encrypted message", required=True)
    e = fields.Expression("Encryption key", required=True)

    template = """
        Decrypt the message `m` given it was encrypted
        with (`e`, `n`).

        <survey :correct="computed.correct" :value="payload.answer">
            Original message: `answer`
        </survey>
    """

    @fields.computed("Decryption key")
    def d(self):
        return pow(self.e, -1, self.totent)

    @fields.computed("Modulo", nohide=True, display_mode=False)
    def n(self):
        return self.p * self.q

    @fields.computed("Totent")
    def totent(self):
        return (self.p - 1) * (self.q - 1)

    @fields.computed("Correct", field=fields.Boolean)
    def correct(self):
        return self.answer == self.m ** self.d % self.n

    def validate(self):
        super().validate()
        if not sympy.isprime(self.p):
            raise ValueError("p is not prime")
        if not sympy.isprime(self.q):
            raise ValueError("q is not prime")
        if self.m > self.n:
            raise ValueError("m should be smaller than n")
        if sympy.gcd(self.e, self.totent) != 1:
            raise ValueError("Non-admissible value for e")

def test_rsa():
    assert not Rsa(m=130, e=13, p=11, q=13, answer=25).correct
    assert Rsa(m=130, e=13, p=11, q=13, answer=26).correct
