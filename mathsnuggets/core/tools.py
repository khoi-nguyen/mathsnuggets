import sympy


def isequal(expr1, expr2, error=0):
    if hasattr(expr1, "doit"):
        expr1 = expr1.doit()
    if hasattr(expr2, "doit"):
        expr2 = expr2.doit()
    expr = sympy.Abs(sympy.nsimplify(expr1) - sympy.nsimplify(expr2))
    if len(expr.atoms(sympy.Symbol)):
        return False
    return expr <= error
