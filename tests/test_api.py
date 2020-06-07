import flask

from app import app


def get(url):
    return app.test_client().get(url)


def post(url, payload):
    return app.test_client().post(
        url, data=flask.json.dumps(payload), content_type="application/json",
    )


def test_widgets():
    response = get("/api/widgets")
    data = flask.json.loads(response.get_data(as_text=True))

    assert response.status_code == 200
    assert isinstance(data, list)
    assert len(data)
    assert "name" in data[0] and "path" in data[0]


def test_field_validation():
    response = post("/api/fields/Equation", {"name": "eq", "value": "x^2"})
    data = flask.json.loads(response.get_data(as_text=True))
    assert response.status_code == 200
    assert data["valid"]

    response = post("/api/fields/Equation", {"name": "eq", "value": "/"})
    data = flask.json.loads(response.get_data(as_text=True))
    assert response.status_code == 400


def test_widget():
    response = get("/api/widgets/Equation")
    data = flask.json.loads(response.get_data(as_text=True))

    assert response.status_code == 200
    assert isinstance(data, list)


def test_widget_validation():
    response = post("/api/widgets/Equation", {"equation": "x^2"})
    data = flask.json.loads(response.get_data(as_text=True))

    assert response.status_code == 200
    assert data["solution"]["value"] == "FiniteSet(0)"


def test_static_routes():
    for route in ["/docs/", "/_static/jquery.js"]:
        response = get(route)
        assert response.status_code == 200
