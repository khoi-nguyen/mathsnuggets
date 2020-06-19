"""
======
Parser
======
"""
from tokenize import TokenError

import sympy
from sympy.parsing.sympy_parser import (
    convert_xor,
    function_exponentiation,
    implicit_multiplication_application,
    parse_expr,
    standard_transformations,
)


def parse(expr, evaluate=False):
    """SymPy expression parser"""
    if isinstance(expr, sympy.Basic):
        return expr
    if isinstance(expr, bool) or not isinstance(expr, (int, float, str, tuple, list)):
        raise TypeError(f"{repr(expr)} is not of an appropriate type: {type(expr)}")
    expr = str(expr)
    if "=" in expr:
        sides = expr.split("=")
        if len(sides) == 1 or any([s.isspace() or not s for s in sides]):
            raise ValueError(f"{repr(expr)} is not a valid equation")
        sides = [parse(s) for s in sides]
        system = sympy.Tuple(
            *[
                sympy.Eq(sides[i], sides[i + 1], evaluate=False)
                for i in range(len(sides) - 1)
            ]
        )
        return system[0] if len(system) == 1 else system
    transformations = standard_transformations + (
        convert_xor,
        implicit_multiplication_application,
        function_exponentiation,
    )
    try:
        result = parse_expr(expr, transformations=transformations, evaluate=evaluate)
    except (SyntaxError, TokenError, RecursionError):
        raise ValueError(f"{repr(expr)} is not a valid mathematical expression.")
    return result
