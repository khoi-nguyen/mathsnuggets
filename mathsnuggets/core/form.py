"""
====
Form
====
"""
import re
from textwrap import dedent

import numpy as np
from pypandoc import convert_text
from sympy import Basic, latex

from mathsnuggets.core import fields
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

    def __init__(self):
        """Fill in the form with default values"""
        for name, field in self.export(False).items():
            if "value" in field:
                setattr(self, name, field["value"])

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
        fields = self.export(False)
        constraints = [n for (n, f) in fields.items() if f.get("constraint")]
        random = [
            n for (n, f) in fields.items() if f.get("random") and not f.get("is_list")
        ]
        random_list = [n for (n, f) in fields.items() if f.get("is_list")]
        while True:
            # TODO: Improve this
            if random_list:
                self._random = {
                    random_list[0]: [int(n) for n in np.random.randint(10, 20, size=15)]
                }
            else:
                values = np.random.randint(-10, 10, len(random))
                values = [parse(str(n)) for n in values]
                self._random = dict(zip(random, values))
            if all([getattr(self, c) for c in constraints]):
                break
        if hasattr(self, "generator") and callable(self.generator):
            self.generator()

    def _is_valid(self):
        if hasattr(self, "validate"):
            try:
                self.validate()
            except (AttributeError, ValueError, TypeError):
                return False
        required = [n for (n, f) in self.export(False).items() if f.get("required")]
        missing = [f for f in required if getattr(self, f) is None]
        return not any(missing)

    def _is_field(self, name, cls=fields.Field):
        return isinstance(getattr(type(self), name), cls)

    def export(self, export_values=True, use_template=False):
        """Get a dictionary of a form's fields

        This is mostly used for communication with the front-end.
        Example of such scenarios include:

        - Getting the fields' list to display in the browser.
        - Getting the values of all *computed* fields
          (e.g. after calling a solver).
        - Getting the fields' values to know
          how the generator filled the form.

        Parameters
        ----------
        export_values : bool
            Whether we should export the fields' values
            (e.g. solutions and completed fields).
        use_template: bool
            Whether to use the form's `template`
            to provide context about the field
            (e.g. surrounding text).

        Todo
        ----
        There should not be any field-specific logic in this function.
        It should be delegated to the fields,
        who should specify how they should be exported.

        Returns
        -------
        dict
            Returns the names of all the form's fields with their respective data.
        """
        cls = type(self)
        fields_info = {
            n: getattr(cls, n).export() for n in dir(self) if self._is_field(n)
        }
        if export_values and self._is_valid():
            for name, field in fields_info.items():
                value = getattr(self, name)
                field["html"] = str(value)
                if isinstance(value, Basic):
                    field["html"] = latex(value)
                    field["value"] = str(value)
        if not use_template:
            return fields_info
        fields_list, before = [], ""
        template = convert_text(dedent(self.template), "html", format="md")[3:-5]
        for part in re.split("</?code>", template):
            if part in fields_info:
                field = fields_info[part]
                field["before"] = before
                fields_list.append(field)
            else:
                before = part
        if part == before:
            fields_list[-1]["after"] = part
        constraints = [f for f in fields_info.values() if f["type"] == "Constraint"]
        constraints.sort(key=lambda f: f["order"])
        return fields_list + constraints
