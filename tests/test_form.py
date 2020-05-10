from mathsnuggets.core import fields, form


class CustomForm(form.Form):
    name = "foobar"
    equation = fields.Equation("Equation")

    first = fields.Field("First", order="_")
    alpha = fields.Field("Starts with A")
    last = fields.Field("Last", order="z")

    template = "Solve `equation`"

    required = fields.Field("Required field", required=True)
    required_2 = fields.Field("Required field", required=True)

    def validate(self):
        if str(self.equation) != "Eq(x**2, 0)":
            raise AttributeError("Wrong equation")

    def solve(self):
        return "Solution"

    public = "Public"
    _private = "Should not be exported"


form = CustomForm()


def test_validate():
    form.required = "Hello"

    assert form.required_2 is None
    assert not form._is_valid()

    form.required_2 = "Hello"
    assert not form._is_valid()

    form.equation = "x^2"
    assert form._is_valid()


def test_export():
    assert form._is_valid()
    export = form.export(True)
    assert "_private" not in export.keys()

    export = form.export(True, True)
    assert len(export) == 1
