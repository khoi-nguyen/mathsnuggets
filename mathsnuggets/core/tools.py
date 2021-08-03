import sympy


def isequal(expr1, expr2, error=0):
    return (
        sympy.Abs(sympy.nsimplify(expr1.doit()) - sympy.nsimplify(expr2.doit()))
        <= error
    )
