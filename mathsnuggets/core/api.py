import os
import traceback
import uuid

import flask
import flask_login
import flask_socketio

from mathsnuggets import widgets
from mathsnuggets.core import cache, fields, form, models

api = flask.Blueprint("api", __name__)

socketio = flask_socketio.SocketIO(cors_allowed_origins="*")

widget_names = [n for n in dir(widgets) if n[0].isupper() and n[1].islower()]
widget_data = [{"path": n, "name": getattr(widgets, n).__doc__} for n in widget_names]


def is_post():
    return flask.request.method == "POST"


@api.route("/widgets")
@cache.cached()
def form_list():
    return flask.jsonify(widget_data)


@api.route("/surveys/<survey>", methods=["GET"])
def count_votes(survey):
    return flask.jsonify([dict(s) for s in models.Vote.find({"survey": survey})])


@api.route("/surveys/<survey>", methods=["DELETE"])
@flask_login.login_required
def delete_votes(survey):
    for vote in models.Vote.find({"survey": survey}):
        vote.delete()
    return flask.jsonify({"success": True})


@api.route("/surveys/<survey>", methods=["POST"])
def cast_vote(survey):
    user = str(flask.request.cookies.get("voter_id"))
    vote = models.Vote(user=user, survey=survey)
    if not vote.survey:
        vote.user = user
        vote.survey = survey
        vote.edit_count = -1
    vote.edit_count += 1
    payload = flask.request.get_json()
    if not vote.value and vote.edit_count <= payload["maxAttempts"]:
        vote.update(payload)
        socketio.emit(
            "voteReceived",
            {"user": str(vote.user), "value": vote.value, "survey": survey},
            room=survey,
        )
    return flask.jsonify(dict(vote))


@socketio.on("join")
def join(survey):
    flask_socketio.join_room(survey)


@api.route("/slideshows", methods=["GET"])
@cache.memoize()
def list_slideshows():
    return flask.jsonify([dict(s) for s in models.Slideshow.find({})])


@api.route("/slideshows/<path:url>", methods=["GET"])
@cache.memoize()
def load_slideshow(url):
    return flask.jsonify(models.Slideshow(url=url).children)


@api.route("/slideshows/", methods=["POST"])
@api.route("/slideshows/<path:url>", methods=["POST"])
@flask_login.login_required
def save_slideshow(url=False):
    slideshow = models.Slideshow(url=url)
    slideshow.update(flask.request.get_json())
    cache.delete_memoized(list_slideshows)
    cache.delete_memoized(load_slideshow, url)
    return flask.jsonify(dict(slideshow))


@api.route("/slideshows/<path:url>", methods=["DELETE"])
@flask_login.login_required
def delete_slideshow(url):
    slideshow = models.Slideshow(url=url)
    slideshow.delete()
    cache.delete_memoized(list_slideshows)
    cache.delete_memoized(load_slideshow, url)
    return "", 204


@api.route("/fields/<field>", methods=["GET"])
@cache.cached(query_string=True)
def validate_field(field):
    payload = flask.request.args
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


@api.route("/widgets/<path:widget>", methods=["GET", "POST"])
@cache.cached(unless=is_post, query_string=True)
def form_route(widget):
    payload = flask.request.args or flask.request.get_json()
    if widget not in widget_names:
        raise InvalidUsage(f"Widget {repr(widget)} does not exist", 404, payload)
    try:
        widget = getattr(widgets, widget)(**(payload if payload else {}))
        if is_post():
            widget.generate()
        if payload:
            widget._validate()
            return flask.jsonify(dict(widget))
    except (AttributeError, ValueError, TypeError, PermissionError) as error:
        raise InvalidUsage(str(error), 400, payload)
    return flask.jsonify(
        {
            "template": str(widget),
            "fields": dict(widget._fields()),
            "generator_template": widget._template(
                getattr(widget, "generator_template", "")
            ),
            "constraints": widget.get_fields_as_template("constraint"),
            "random_numbers": widget.get_fields_as_template("random"),
        }
    )


login_manager = flask_login.LoginManager()


@login_manager.user_loader
def load_user(identifier):
    user = models.User(_id=identifier)
    return user if user.email else None


@api.route("/auth/register", methods=["POST"])
def register():
    payload = flask.request.get_json()
    registration_pw = payload.pop("registration_password")
    if registration_pw != os.environ.get("REGISTRATION_PASSWORD", ""):
        raise InvalidUsage("Registration password incorrect", 400, payload)
    user = models.User(email=payload["email"])
    if user.email:
        raise InvalidUsage(f"User {user.email} already exists", 400, payload)
    try:
        user.update(payload)
    except (AttributeError, ValueError) as error:
        raise InvalidUsage(str(error), 400, payload)
    return flask.jsonify({"success": True})


@api.route("/auth/login", methods=["GET", "POST"])
def login():
    payload = flask.request.get_json()
    if not payload:
        user = flask_login.current_user
        voter_id = flask.request.cookies.get("voter_id") or str(uuid.uuid1())
        response = flask.jsonify(
            {
                "is_authenticated": user.is_authenticated,
                "email": getattr(user, "email", False),
                "voter_id": voter_id,
            }
        )
        if not flask.request.cookies.get("voter_id"):
            response.set_cookie("voter_id", voter_id)
        return response
    user = models.User(email=payload["email"])
    if not user.email or not user.check_password(payload["password"]):
        raise InvalidUsage("Incorrect email or password")
    flask_login.login_user(user, remember=payload.get("remember", False))
    return flask.jsonify({"success": True})


@api.route("/auth/nickname", methods=["GET", "POST"])
def update_nickname():
    payload = flask.request.get_json()
    anonymous_id = flask.request.cookies.get("voter_id")
    username = getattr(flask_login.current_user, "email", anonymous_id)
    identity = models.Identity(username=username)
    if payload:
        payload["username"] = username
        identity.update(payload)
    return flask.jsonify(dict(identity))


@api.route("/auth/logout")
@flask_login.login_required
def logout():
    flask_login.logout_user()
    return flask.jsonify({"success": True})


@api.route("/tests")
@cache.cached()
def tests():
    test_data = {v["name"]: v["test"] for k, v in widgets.info.items() if v.get("test")}
    return flask.jsonify(test_data)


@api.route("/tests/user", methods=["DELETE"])
def delete_test_user():
    if "MONGO_URL" not in os.environ:
        user = models.User(email="test@test.com")
        user.delete()
        return "", 204


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
        yield ("traceback", traceback.format_exc())
        yield ("payload", dict(self.payload or ()))
        yield ("message", self.message)


@api.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    response = flask.jsonify(dict(error))
    response.status_code = error.status_code
    return response
