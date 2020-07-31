"""
====
Form
====
"""
import random
import re
import textwrap

from mathsnuggets.core import fields


class Form:
    """Form Template

    All forms should inherit from this class,
    as it performs the following things:

    - Pre-filling with default values (``__init__``)
    - Interactions with the front-end (``export``)
    - Interactions with the generators (``generate``)
    """

    _random = {}

    def __init__(self, **kwargs):
        """Fill in the form with default values"""
        for attr, field in self._fields(lambda f: "default" in f):
            setattr(self, attr, field["default"])
        for attr, value in kwargs.items():
            if attr in dict(iter(self)):
                setattr(self, attr, value)

    def generate(self):
        """Generate an exercise

        - List all random number fields and all the constraints
        - Fill in the random numbers fields until they satisfy the constraints
        - Call the exercise's generator to fill in the rest of the form

        Todo
        ----
        - Allow flexibility for the number ranges
        - Stop the search for appropriate numbers after some time
        - Check for contradictory constraints
        """
        constraints = list(
            self._fields(
                lambda f: f.get("constraint") and not f.get("range_constraint")
            )
        )
        range_constraints = list(self._fields(lambda f: f.get("range_constraint")))
        random_fields = list(self._fields(lambda f: f.get("random")))
        for constraint, _ in range_constraints:
            getattr(type(self), constraint).change_range(self)
        self._random = {}
        while True:
            for attr, _ in random_fields:
                self._random[attr] = random.choice(list(self.__dict__.get(attr)))
            if all([getattr(self, c) for c, _ in constraints]):
                break
        if hasattr(self, "generator") and callable(self.generator):
            self.generator()

    @property
    def valid(self):
        try:
            self._validate()
            return True
        except (ValueError, AttributeError, TypeError, AssertionError):
            return False

    def _validate(self):
        for attr, _ in self._fields(lambda f: f.get("required")):
            if getattr(self, attr) is None:
                raise AttributeError(f"Field {repr(attr)} is required")
        for attr, _ in self._fields(lambda f: f.get("computed")):
            getattr(self, attr)
        if hasattr(self, "validate"):
            self.validate()

    def __iter__(self):
        for attr in dir(self):
            try:
                value = getattr(self, attr)
                assert not attr.startswith("_") and not callable(value)
                yield (attr, value)
            except (ValueError, AttributeError, TypeError, AssertionError):
                continue

    def __str__(self):
        """Transforms the object into a Vue template"""

        def field_to_xml(match):
            field = dict(getattr(type(self), match.group(1)))
            payload = "computed" if field.get("computed") else "payload"
            attrs = {"v-model": f"{payload}.{field['name']}"}
            for prop, val in field.items():
                prop = prop.replace("_", "-")
                if not isinstance(val, str):
                    prop = f":{prop}"
                if val in [True, False]:
                    val = "true" if val else "false"
                attrs[prop] = val
            attrs = " ".join([f'{prop}="{val}"' for prop, val in attrs.items()])
            return f"<form-field {attrs} />"

        return "<div>" + re.sub(r"`([a-z_]+)`", field_to_xml, self.template) + "</div>"

    def _fields(self, callback=None):
        """Iterates through all fields satisfying 'callback'"""
        parts = []
        for attr in self.__dir__():
            # Exclude non-fields
            if not isinstance(getattr(type(self), attr), fields.Field):
                continue
            field_object = getattr(type(self), attr)
            field = dict(field_object)
            # Add value
            try:
                value = getattr(self, attr)
                if field.get("constraint"):
                    value = self.__dict__[attr] if attr in self.__dict__ else False
                assert value is not None
                field.update(field_object.export(value))
            except (ValueError, AttributeError, TypeError, AssertionError):
                pass
            # Check if callback is satisfied
            # Callback may use context, so this is done last
            if callable(callback) and not callback(field):
                continue
            yield (attr, field)
