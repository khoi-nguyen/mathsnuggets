"""
====
Form
====
"""
import textwrap

import numpy

from mathsnuggets.core import db, fields
from mathsnuggets.parser import parse


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
        constraints = self._fields(lambda f: f.get("constraint"))
        random = list(self._fields(lambda f: f.get("random")))
        while True:
            values = numpy.random.randint(-10, 10, len(random))
            values = [parse(str(n)) for n in values]
            self._random = dict(zip(random, values))
            if all([getattr(self, c) for c, _ in constraints]):
                break
        if hasattr(self, "generator") and callable(self.generator):
            self.generator()

    @property
    def valid(self):
        for attr, _ in self._fields(lambda f: f.get("required")):
            if getattr(self, attr) is None:
                return False
        if hasattr(self, "validate"):
            try:
                self.validate()
            except (ValueError, AttributeError, TypeError, AssertionError):
                return False
        return True

    def __iter__(self):
        for attr in dir(self):
            try:
                value = getattr(self, attr)
                assert not attr.startswith("_") and not callable(value)
                yield (attr, value)
            except (ValueError, AttributeError, TypeError, AssertionError):
                continue

    def _fields(self, callback=None):
        """Iterates through all fields satisfying 'callback'"""
        parts = []
        if hasattr(self, "template"):
            parts = textwrap.dedent(self.template).split("`")
        for attr in dir(self):
            # Exclude non-fields
            if not isinstance(getattr(type(self), attr), fields.Field):
                continue
            field_object = getattr(type(self), attr)
            field = dict(field_object)
            # Add context
            if attr in parts:
                pos = parts.index(attr)
                field["order"] = (pos - 1) // 2
                field["before"] = parts[pos - 1]
                if pos == len(parts) - 2:
                    field["after"] = parts[-1]
            # Add value
            try:
                value = getattr(self, attr)
                assert value is not None
                field.update(field_object.export(value))
            except (ValueError, AttributeError, TypeError, AssertionError):
                pass
            # Check if callback is satisfied
            # Callback may use context, so this is done last
            if callable(callback) and not callback(field):
                continue
            yield (attr, field)

    def _save(self):
        if hasattr(self, "_id") and hasattr(self, "_position"):
            db.slideshows.update_one(
                {"_id": self._id}, {"$set": {self._position: dict(iter(self))}}
            )
