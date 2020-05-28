"""
BACK-END
========
"""

import flask

from mathsnuggets import widgets
from mathsnuggets.core import fields, form

app = flask.Flask(__name__)
widget_names = [n for n in dir(widgets) if n[0].isupper() and n[1].islower()]
widget_data = [{"path": n, "name": getattr(widgets, n).__doc__} for n in widget_names]


def form_patch(form, constraint):
    return {
        name: {key: field[key] for key in field.keys() if key in ["value", "html"]}
        for (name, field) in form.export().items()
        if constraint(field)
    }


@app.route("/_components")
def form_list():
    return flask.jsonify(widget_data)


@app.route("/_field/<field>", methods=["POST"])
def validate_field(field):
    # TODO: error handling
    field_cls = getattr(fields, field)
    data = flask.request.get_json()
    value = data.pop("value")
    kwargs = {k: v for k, v in data.items() if k not in field_cls._blacklist}

    class DummyForm(form.Form):
        field = field_cls("Dummy Field", **kwargs)

    return flask.jsonify(DummyForm.field.validate(value))


@app.route("/_form/<path:form>", methods=["GET", "POST"])
@app.route("/_form/<path:form>/<generator>", methods=["GET", "POST"])
def form_route(form, generator=False):
    if form not in widget_names:
        flask.abort(404)
    form = getattr(widgets, form)()
    # Getting fieds data and filling the form if necessary
    if flask.request.get_json() or generator:
        for field, value in flask.request.get_json().items():
            try:
                setattr(form, field, value)
            except AttributeError:
                raise AttributeError(
                    f"Value {repr(value)} invalid "
                    + f"for field {repr(field)} in {form.__doc__}",
                )
        if generator:
            form.generate()

            def constraint(field):
                return not field.get("random") and not field.get("constraint")

        else:

            def constraint(field):
                return field.get("computed")

        return flask.jsonify(form_patch(form, constraint))
    data = form.export(False, True)
    return flask.jsonify(data)


@app.route("/")
@app.route("/<path:path>")
def default(path="index.html"):
    folder = "dist/"
    if path.startswith("docs/"):
        folder = "docs/build/html/"
        path = path[5:] if len(path) > 5 else "index.html"
    elif path.startswith("_static"):
        folder = "docs/build/html/"
    slash = path.rfind("/") + 1
    return flask.send_from_directory(f"{folder}/{path[:slash]}", path[slash:])


# TODO: Cleaner error handling: if _url, json
@app.errorhandler(Exception)
def handle_exception(exception):
    return flask.jsonify({"error": True, "errormessage": str(exception)})


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
