"""
====
Form
====
"""
import random
import re
import uuid

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
            if attr in dict(self._fields()):
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

    def _validate(self):
        for attr, _ in self._fields(lambda f: f.get("required")):
            if getattr(self, attr) is None:
                raise AttributeError(f"Field {repr(attr)} is required")
        for attr, _ in self._fields(lambda f: f.get("computed")):
            getattr(self, attr)
        if hasattr(self, "validate"):
            self.validate()

    def __iter__(self):
        for attr, _ in self._fields(
            lambda f: not f.get("random") and not f.get("constraint")
        ):
            export = getattr(type(self), attr).export
            value = getattr(self, attr, None)
            if value is None:
                continue
            yield (attr, export(value).get("value"))

    def __str__(self):
        """Transforms the object into a Vue template"""
        return self._template(self.template)

    def _template(self, string):
        def option_to_field(match):
            field = dict(getattr(type(self), match.group(1)))
            return f"""
                <config-option name="{field['label']}">
                    `{match.group(1)}`
                </config-option>
            """
        string = re.sub(r"~([a-zA-Z0-9_]*)~", option_to_field, string)

        def field_to_xml(match):
            field = dict(getattr(type(self), match.group(1)))
            payload = "computed" if field.get("computed") else "payload"
            attrs = {
                "v-model": f"{payload}.{field['name']}",
                ":editable": "config.edit",
            }
            for prop, val in field.items():
                prop = prop.replace("_", "-")
                if not isinstance(val, str):
                    prop = f":{prop}"
                if val in [True, False]:
                    val = "true" if val else "false"
                attrs[prop] = val
            attrs = " ".join([f'{prop}="{val}"' for prop, val in attrs.items()])
            return f"<form-field {attrs} />"

        return "<div>" + re.sub(r"`([a-zA-Z0-9_]*)`", field_to_xml, string) + "</div>"

    def get_fields_as_template(self, field_type):
        fields = [f"`{attr}`" for attr, _ in self._fields(lambda f: f.get(field_type))]
        return self._template(" ".join(fields))

    def _fields(self, callback=None):
        """Iterates through all fields satisfying 'callback'"""
        for attr in self.__dir__():
            if not hasattr(type(self), attr) or not isinstance(
                getattr(type(self), attr), fields.Field
            ):
                continue
            field = dict(getattr(type(self), attr))
            if callable(callback) and not callback(field):
                continue
            yield (attr, field)


class MarkedForm(Form):
    name = fields.Field("Form identifier")

    def validate(self):
        if not self.name:
            self.name = str(uuid.uuid1())
