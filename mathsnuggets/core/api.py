import bson.objectid
import flask
import flask_login

from mathsnuggets import widgets
from mathsnuggets.core import db, fields, form, models

api = flask.Blueprint("api", __name__)

widget_names = [n for n in dir(widgets) if n[0].isupper() and n[1].islower()]
widget_data = [{"path": n, "name": getattr(widgets, n).__doc__} for n in widget_names]


@api.route("/widgets")
def form_list():
    return flask.jsonify(widget_data)


@api.route("/slideshows")
def list_slideshows(identifier=False):
    slideshows = db.slideshows.aggregate(
        [
            {
                "$match": {"_id": bson.objectid.ObjectId(identifier)}
                if identifier
                else {}
            },
            {
                "$project": {
                    "_id": False,
                    "id": {"$toString": "$_id"},
                    "title": True,
                    "date": True,
                    "authors": True,
                }
            },
        ]
    )
    slideshows = list(slideshows)
    if identifier:
        return flask.jsonify(slideshows[0])
    return flask.jsonify(slideshows)


@api.route("/slideshows/<identifier>", methods=["GET"])
def load_slideshow(identifier):
    query = {"_id": bson.objectid.ObjectId(identifier)}
    slideshow = models.Slideshow(**query)
    return flask.jsonify(dict(slideshow)["slides"])


@api.route("/slideshows/", methods=["POST"])
@api.route("/slideshows/<identifier>", methods=["POST"])
@flask_login.login_required
def save_slideshow(identifier=False):
    post = flask.request.get_json()
    if not identifier:
        post["slides"] = []
        _id = db.slideshows.insert_one(post)
        return list_slideshows(str(_id.inserted_id))
    query = {"_id": bson.objectid.ObjectId(identifier)}
    slideshow = db.slideshows.find_one(query)
    if "key" in post:
        if slideshow:
            new_vals = {"$set": {post["key"]: post["patch"]}}
        else:
            new_vals = {"$set": {"slides": [post["patch"]]}}
    else:
        new_vals = {"$set": post}
    db.slideshows.update_one(query, new_vals, upsert=True)
    if "key" not in post:
        return list_slideshows(identifier)
    return flask.jsonify({"success": True})


@api.route("/fields/<field>", methods=["POST"])
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


@api.route("/widgets/<path:form>", methods=["GET", "POST"])
@api.route("/widgets/<path:form>/<generator>", methods=["GET", "POST"])
def form_route(form, generator=False):
    payload = flask.request.get_json()
    if form not in widget_names:
        raise InvalidUsage(f"Widget {repr(form)} does not exist", 404, payload)
    try:
        form = getattr(widgets, form)(**(payload if payload else {}))
        if generator:
            form.generate()
        if payload:
            form._validate()
            return flask.jsonify(dict(form._fields()))
    except (AttributeError, ValueError, TypeError, PermissionError) as error:
        raise InvalidUsage(str(error), 400, payload)
    data = [f for n, f in form._fields()]
    data.sort(key=lambda f: f.get("order"))
    return flask.jsonify(data)


login_manager = flask_login.LoginManager()


@login_manager.user_loader
def load_user(identifier):
    user = models.User(_id=bson.objectid.ObjectId(identifier))
    return user if user.email else None


@api.route("/auth/register", methods=["POST"])
def register():
    payload = flask.request.get_json()
    user = models.User(email=payload["email"])
    if user.email:
        raise InvalidUsage(f"User {user.email} already exists", 400, payload)
    try:
        user.email = payload["email"]
        user.password = payload["password"]
    except (AttributeError, ValueError) as error:
        raise InvalidUsage(str(error), 400, payload)
    user.save()
    return flask.jsonify({"success": True})


@api.route("/auth/login", methods=["GET", "POST"])
def login():
    payload = flask.request.get_json()
    if not payload:
        return {"is_authenticated": flask_login.current_user.is_authenticated}
    user = models.User(email=payload["email"])
    if not user.email or not user.check_password(payload["password"]):
        raise InvalidUsage("Incorrect email or password")
    flask_login.login_user(user)
    return flask.jsonify({"success": True})


@api.route("/auth/logout")
@flask_login.login_required
def logout():
    flask_login.logout_user()
    return flask.jsonify({"success": True})


class InvalidUsage(Exception):
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        super().__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def __iter__(self):
        yield ("error", True)
        yield ("status_code", self.status_code)
        yield ("payload", dict(self.payload or ()))
        yield ("message", self.message)


@api.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    response = flask.jsonify(dict(error))
    response.status_code = error.status_code
    return response
