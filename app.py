"""
BACK-END
========
"""
import flask

from mathsnuggets import widgets
from mathsnuggets.core import db, fields, form

app = flask.Flask(__name__)
widget_names = [n for n in dir(widgets) if n[0].isupper() and n[1].islower()]
widget_data = [{"path": n, "name": getattr(widgets, n).__doc__} for n in widget_names]


@app.route("/api/widgets")
def form_list():
    return flask.jsonify(widget_data)


@app.route("/api/slideshows")
def get_slideshow():
    slideshow = db.slideshows.find_one()
    slides = slideshow["slides"] if slideshow else [{"title": ""}]
    for slide in slides:
        if "widgets" not in slide:
            slide["widgets"] = [[{"type": "", "fields": []}]]
            continue
        for col in slide["widgets"]:
            for widget in col:
                if "fields" not in widget:
                    continue
                form = getattr(widgets, widget["type"])(**widget["fields"])
                data = [f for n, f in form._fields()]
                data.sort(key=lambda f: f.get("order"))
                widget["fields"] = data
    return flask.jsonify(slides)


@app.route("/api/slideshows/save", methods=["POST"])
def save_slideshow():
    post = flask.request.get_json()
    slideshow = db.slideshows.find_one()
    if slideshow:
        new_vals = {"$set": {post["key"]: post["patch"]}}
    else:
        new_vals = {"$set": {"slides": [post["patch"]]}}
    db.slideshows.update_one({}, new_vals, upsert=True)
    return flask.jsonify([post, new_vals])


@app.route("/api/fields/<field>", methods=["POST"])
def validate_field(field):
    payload = flask.request.get_json()
    if not hasattr(fields, field):
        raise InvalidUsage(f"Field {repr(field)} does not exist", 404, payload=payload)
    if "value" not in payload:
        raise InvalidUsage("Missing 'value' field in payload", payload=payload)
    field_cls = getattr(fields, field)
    value = payload.get("value")
    kwargs = {k: v for k, v in payload.items() if k not in field_cls._blacklist}

    class DummyForm(form.Form):
        field = field_cls("Dummy Field", **kwargs)

    try:
        response = DummyForm.field.validate(value)
        return flask.jsonify(response)
    except (ValueError, TypeError, AttributeError) as error:
        raise InvalidUsage(str(error), 400, payload)


@app.route("/api/widgets/<path:form>", methods=["GET", "POST"])
@app.route("/api/widgets/<path:form>/<generator>", methods=["GET", "POST"])
def form_route(form, generator=False):
    payload = flask.request.get_json()
    if form not in widget_names:
        raise InvalidUsage(f"Widget {repr(form)} does not exist", 404, payload)
    try:
        form = getattr(widgets, form)(**(payload if payload else {}))
    except (AttributeError, ValueError, TypeError) as error:
        raise InvalidUsage(str(error), 400, payload)
    if generator:
        form.generate()
    if payload:
        return flask.jsonify(dict(form._fields()))
    data = [f for n, f in form._fields()]
    data.sort(key=lambda f: f.get("order"))
    return flask.jsonify(data)


@app.route("/about")
@app.route("/plot")
@app.route("/slideshow_builder")
def frontend():
    return flask.send_from_directory("dist/", "index.html")


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


class InvalidUsage(Exception):
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        super().__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def __iter__(self):
        yield ("status_code", self.status_code)
        yield ("payload", dict(self.payload or ()))
        yield ("message", self.message)


@app.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    response = flask.jsonify(dict(error))
    response.status_code = error.status_code
    return response


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
