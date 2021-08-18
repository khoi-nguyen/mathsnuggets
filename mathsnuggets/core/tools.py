import sympy


def isequal(expr1, expr2, error=0):
    expr = sympy.Abs(sympy.nsimplify(expr1.doit()) - sympy.nsimplify(expr2.doit()))
    if len(expr.atoms(sympy.Symbol)):
        return False
    return expr <= error
