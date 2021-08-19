"""
======
Parser
======
"""
import tokenize

import sympy
from sympy.parsing.sympy_parser import (
    auto_symbol,
    convert_xor,
    factorial_notation,
    function_exponentiation,
    implicit_multiplication_application,
    lambda_notation,
    parse_expr,
    repeated_decimals,
)


def simplify(expr):
    if hasattr(expr, "func") and expr.func == sympy.Mul:
        sign = 1
        args = list(expr.args)
        for index, term in enumerate(args):
            if term.is_number and term.is_negative:
                args[index] *= -1
                sign *= -1
        return sympy.Mul(sign, sympy.Mul(*args, evaluate=False), evaluate=False)
    elif hasattr(expr, "args") and len(expr.args) > 1:
        blacklist = [sympy.Integral, sympy.Tuple]
        params = {} if expr.func in blacklist else {"evaluate": False}
        return expr.func(*[simplify(arg) for arg in expr.args], **params)
    else:
        return expr


def auto_number(tokens, local_dict, global_dict):
    result = []
    for (toknum, tokval), next_tok in zip(tokens, tokens[1:]):
        if toknum == tokenize.NUMBER:
            number = tokval
            postfix = []

            if number.endswith("j") or number.endswith("J"):
                number = number[:-1]
                postfix = [(tokenize.OP, "*"), (tokenize.NAME, "I")]

            if "e" in number or "E" in number:
                index = max(number.find("E"), number.find("e"))
                mantissa, power = number[0:index], number[index + 1 :]
                seq = [
                    (tokenize.NAME, "Float"),
                    (tokenize.OP, "("),
                    (tokenize.NUMBER, repr(mantissa)),
                    (tokenize.OP, ")"),
                    (tokenize.OP, "*"),
                    (tokenize.NAME, "UnevaluatedExpr"),
                    (tokenize.OP, "("),
                    (tokenize.NUMBER, "10"),
                    (tokenize.OP, ")"),
                    (tokenize.OP, "**"),
                    (tokenize.NUMBER, power),
                ]
            elif "." in number and not (
                number.startswith("0x") or number.startswith("0X")
            ):
                seq = [
                    (tokenize.NAME, "Float"),
                    (tokenize.OP, "("),
                    (tokenize.NUMBER, repr(str(number))),
                    (tokenize.OP, ")"),
                ]
            elif str(tokval) == "10" and next_tok in [
                (tokenize.OP, "^"),
                (tokenize.OP, "**"),
            ]:
                seq = [
                    (tokenize.NAME, "UnevaluatedExpr"),
                    (tokenize.OP, "("),
                    (tokenize.NUMBER, "10"),
                    (tokenize.OP, ")"),
                ]
            else:
                seq = [
                    (tokenize.NAME, "Integer"),
                    (tokenize.OP, "("),
                    (tokenize.NUMBER, number),
                    (tokenize.OP, ")"),
                ]

            result.extend(seq + postfix)
        else:
            result.append((toknum, tokval))

    return result


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
    transformations = (
        lambda_notation,
        auto_symbol,
        repeated_decimals,
        auto_number,
        factorial_notation,
        convert_xor,
        implicit_multiplication_application,
        function_exponentiation,
    )
    try:
        result = simplify(
            parse_expr(expr, transformations=transformations, evaluate=evaluate)
        )
    except (SyntaxError, tokenize.TokenError, RecursionError):
        raise ValueError(f"{repr(expr)} is not a valid mathematical expression.")
    return result
