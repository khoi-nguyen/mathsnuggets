"""
BACK-END
========
"""
import os

import flask

from mathsnuggets.core import api, cache

app = flask.Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "hello").encode("UTF-8")
app.register_blueprint(api.api, url_prefix="/api")
api.login_manager.init_app(app)
api.socketio.init_app(app)
cache.cache.init_app(app)


@app.route("/login")
@app.route("/resources")
@app.route("/resources/")
@app.route("/resources/<path:identifier>")
def frontend(identifier=False):
    return flask.send_from_directory("dist/", "index.html")


@app.route("/")
@app.route("/<path:path>")
def default(path="index.html"):
    folder = "dist/"
    if path.startswith("docs/"):
        folder = "docs/build/html/"
        path = path[5:] if len(path) > 5 else "index.html"
    elif path.startswith("storage/"):
        folder = os.environ.get("STORAGE", "./storage/")
        path = path[8:]
    elif path.startswith("_static"):
        folder = "docs/build/html/"
    elif path == "favicon.ico":
        folder = "static/"
    slash = path.rfind("/") + 1
    return flask.send_from_directory(f"{folder}/{path[:slash]}", path[slash:])


def init():
    if __name__ == "__main__":
        api.socketio.run(app, debug=True)


init()
