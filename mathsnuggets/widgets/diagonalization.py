import sympy

from mathsnuggets.core import fields, form


class Diagonalization(form.Form):
    """Diagonalization"""

    matrix = fields.Matrix("Matrix")

    template = """
        Matrix: `matrix`

        Characteristic polynomial
        `characteristic_polynomial`

        Diagonalization
        `diagonalize`
    """

    @fields.computed("Characteristic polynomial")
    def characteristic_polynomial(self):
        lam = sympy.symbols("lambda")
        n = self.matrix.shape[0]
        poly = (self.matrix - lam * sympy.eye(n)).det()
        return sympy.Eq(poly, sympy.factor(poly), evaluate=False)

    @fields.computed("Diagonalization")
    def diagonalize(self):
        p, d = self.matrix.diagonalize(normalize=True)
        if self.matrix == sympy.Transpose(self.matrix):
            basis = sympy.GramSchmidt(p.columnspace(), True)
            p = basis[0]
            for i in range(1, len(basis)):
                p = p.col_insert(i, basis[i])
        return [p, d, p ** -1]
