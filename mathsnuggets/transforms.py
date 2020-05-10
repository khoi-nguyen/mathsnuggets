"""
==========
Transforms
==========
"""
from sympy import I, Symbol, oo
from sympy.core.facts import InconsistentAssumptions


def make_real(expr):
    """Attempts to transform a Sympy expression to one which is real"""
    if expr.atoms(I, oo, -oo):
        raise ValueError(
            f"{repr(expr)} contains a problematic symbol" + repr(expr.atoms(I, oo, -oo))
        )

    # Add real=True to all symbols if possible
    for old_symbol in expr.atoms(Symbol):
        assumptions = old_symbol.assumptions0
        assumptions["real"] = True
        try:
            symbol = Symbol(old_symbol.name, **assumptions)
        except InconsistentAssumptions:
            raise ValueError(
                f"Symbol {repr(old_symbol)} in {repr(expr)} has an assumption"
                + "that prevents it from being made real"
            )
        expr = expr.replace(old_symbol, symbol)
    return expr
