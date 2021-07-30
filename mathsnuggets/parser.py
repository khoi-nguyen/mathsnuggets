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


def simplify(expr):
    if expr.func == sympy.Mul:
        sign = 1
        args = list(expr.args)
        for index, term in enumerate(args):
            if term.is_number and term.is_negative:
                args[index] *= -1
                sign *= -1
        return sympy.Mul(sign, sympy.Mul(*args, evaluate=False), evaluate=False)
    elif len(expr.args) > 1:
        return expr.func(*[simplify(arg) for arg in expr.args], evaluate=False)
    else:
        return expr


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
        result = simplify(
            parse_expr(expr, transformations=transformations, evaluate=evaluate)
        )
    except (SyntaxError, TokenError, RecursionError):
        raise ValueError(f"{repr(expr)} is not a valid mathematical expression.")
    return result
