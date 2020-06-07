"""
BACK-END
========
"""
import flask

from mathsnuggets.core import api

app = flask.Flask(__name__)
app.register_blueprint(api.api, url_prefix="/api")


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


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
