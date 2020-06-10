"""
======
Fields
======
"""
import re

import bcrypt
import pypandoc
import sympy

from mathsnuggets.parser import parse


class Field:
    """Basic field descriptor

    The idea of fields is to use them as class attributes when coding,
    but they should also contain useful information for web display.
    As an example, a field ``equation`` should only be manipulated
    as a (SymPy) mathematical equation, but when exported, it should
    contain additional information (metadata) for the front-end.

    Fields' values are usually set by the end user
    and therefore also need to be validated.

    In other words, the role of this class is:

    - Store a field's metadata (name, label, default value, etc.).
      This is done in ``__init__``
    - Validate what the end user inputs (``validate``)
    - Export the metadata for the front-end

    Attributes
    ----------
    name : str
        Name of the field (backend, html)
    label : str
        Label for the front-end
    """

    _blacklist = [
        "_blacklist",
        "construct",
        "label",
        "name",
        "sanitize",
        "type",
        "validate",
    ]

    def __get__(self, instance, owner):
        if instance is None:
            return self
        if hasattr(self, "callback"):
            return self.callback(instance)
        return instance.__dict__[self.name] if self.name in instance.__dict__ else None

    def __init__(self, label, *args, **kwargs):
        self.label = label
        self.type = self.__class__.__name__
        invalid_keys = [repr(k) for k in kwargs if k in self._blacklist]
        if invalid_keys:
            raise KeyError(f"Invalid kwargs for {repr(self)}: {repr(invalid_keys)}")
        for key, val in kwargs.items():
            setattr(self, key, val)
        if hasattr(self, "construct"):
            self.construct(*args, **kwargs)

    def __set__(self, instance, value):
        if (
            hasattr(self, "protected")
            and self.protected
            and (not hasattr(self, "default") or value != self.default)
        ):
            raise PermissionError(f"Field {repr(self.name)} is protected")
        value = self.sanitize(value)
        instance.__dict__[self.name] = value

    def __set_name__(self, owner, name):
        self.name = name

    def __iter__(self):
        """Export field attributes"""
        for attr in dir(self):
            value = getattr(self, attr)
            if not attr.startswith("_") and not callable(value):
                yield (attr, value)

    def sanitize(self, value):
        return value

    def validate(self, value):
        """Determines whether value is appropriate for the field"""
        value = self.sanitize(value)
        return self.export(value)

    def export(self, value):
        return {"value": value, "valid": True if value else False}


def computed(*args, **kwargs):
    """Decorator to create a Field from a method"""

    field = kwargs["field"] if "field" in kwargs else Expression

    def decorator(function):
        class ComputedField(field):
            """Computed Field"""

            computed = True
            callback = staticmethod(function)

        return ComputedField(*args, **kwargs)

    return decorator


class Expression(Field):
    """Mathematical expression"""

    def sanitize(self, expr):
        """Transform expr into a real mathematical expression"""
        return parse(expr)

    def export(self, value):
        return {
            "value": f"{value}",
            "latex": sympy.latex(value),
            "valid": value is not None,
        }


class Matrix(Expression):
    def sanitize(self, expr):
        return sympy.Matrix(sympy.parse_expr(expr))


class Equation(Expression):
    """Equation field"""

    def sanitize(self, equation):
        """Transform string to a SymPy equality or a tuple of them"""
        equation = parse(equation)
        if equation.func == sympy.Tuple:
            return equation.func(*[self.sanitize(eq) for eq in equation.args])
        if equation.func != sympy.Eq:
            equation = sympy.Eq(equation, 0, evaluate=False)
        return equation


class RandomNumber(Field):
    """Random Number field"""

    default = "-10, 10"
    hidden = True
    random = True

    def callback(self, instance):
        """Get the value from the form's _random attribute"""
        if "_random" in instance.__dict__ and self.name in instance.__dict__["_random"]:
            return instance.__dict__["_random"][self.name]
        if self.name in instance.__dict__:
            return instance.__dict__[self.name]
        return None

    def export(self, instance):
        return {}

    def sanitize(self, expr):
        """Check it is an appropriate range"""
        if isinstance(expr, (tuple, list)):
            return list(expr)
        try:
            numbers = [int(n) for n in str(expr).split(",")]
            assert len(numbers) > 0
            if len(numbers) > 1:
                assert numbers[1] >= numbers[0]
                assert len(numbers) == 2
            else:
                numbers.append(numbers[0] + 1)
        except (AssertionError, ValueError):
            raise ValueError(f"{repr(expr)} is not a valid expression for {self.name}")
        return list(range(*numbers))


class Constraint(Field):
    """Constraint"""

    constraint = True
    default = False
    range_constraint = False

    def sanitize(self, expr):
        return bool(expr)

    def export(self, value):
        return {}


def constraint(*args, **kwargs):
    # if set to False, get -> lambda x : True
    # set_val = instance.__dict__[self.name]
    # if true, computedField
    def decorator(method):
        class DecoratedConstraint(Constraint):
            def callback(self, form):
                if self.name not in form.__dict__ or not form.__dict__[self.name]:
                    return True
                return method(form)

        return DecoratedConstraint(*args, **kwargs)

    return decorator


def range_constraint(*args, **kwargs):
    def decorator(method):
        class DecoratedConstraint(Constraint):
            range_constraint = True

            def change_range(self, form):
                if self.name in form.__dict__ and form.__dict__[self.name]:
                    method(form)

        return DecoratedConstraint(*args, **kwargs)

    return decorator


class Html(Field):
    def export(self, value):
        return {"html": value, "valid": True if value else False}


class Markdown(Field):
    """Equation field"""

    fmt = "{value}"

    def sanitize(self, value):
        """Transform markdown to HTML"""
        return pypandoc.convert_text(self.fmt.format(value=value), "html", format="md")

    def export(self, value):
        return {
            "html": value,
            "value": pypandoc.convert_text(value, "md", format="html"),
            "valid": value != "",
        }


class Email(Field):
    """Email Field"""

    def sanitize(self, value):
        if not re.search(r"^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$", value):
            raise ValueError("Invalid email address")
        return value


class Password(Field):
    """Password field"""

    def sanitize(self, value):
        if not value:
            raise ValueError("Password field cannot be empty")
        if len(value) <= 7:
            raise ValueError("A valid password must have at least 8 characters")
        return bcrypt.hashpw(value.encode("utf8"), bcrypt.gensalt())

    @staticmethod
    def check(value, hashed):
        return bcrypt.checkpw(value.encode("utf8"), hashed)
