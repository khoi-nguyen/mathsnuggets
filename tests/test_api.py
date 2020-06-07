import flask

from app import app


def get(url, get_data=True):
    response = app.test_client().get(url)
    if not get_data:
        return response
    data = flask.json.loads(response.get_data(as_text=True))
    return (response, data)


def post(url, payload):
    response = app.test_client().post(
        url, data=flask.json.dumps(payload), content_type="application/json",
    )
    data = flask.json.loads(response.get_data(as_text=True))
    return (response, data)


def test_widgets():
    response, data = get("/api/widgets")

    assert response.status_code == 200
    assert isinstance(data, list)
    assert len(data)
    assert "name" in data[0] and "path" in data[0]


def test_field_validation():
    response, data = post("/api/fields/Equation", {"name": "eq", "value": "x^2"})
    assert response.status_code == 200
    assert data["valid"]

    response, data = post("/api/fields/Equation", {"name": "eq", "value": "/"})
    assert response.status_code == 400

    response, data = post("/api/fields/Eequation", {"name": "eq", "value": "/"})
    assert response.status_code == 404

    response, data = post("/api/fields/Equation", {"name": "eq"})
    assert response.status_code == 400


def test_widget():
    response, data = get("/api/widgets/Equation")
    assert response.status_code == 200
    assert isinstance(data, list)

    response, data = get("/api/widgets/Eequation")
    assert response.status_code == 404


def test_widget_validation():
    response, data = post("/api/widgets/Equation", {"equation": "x^2"})

    assert response.status_code == 200
    assert data["solution"]["value"] == "FiniteSet(0)"

    response, data = post("/api/widgets/Equation", {"equation": "sin("})
    assert response.status_code == 400

    response, data = post("/api/widgets/Equation", {"x": "x"})
    assert response.status_code == 400


def test_retrieve_slideshow():
    response, data = get("/api/slideshows")
    assert response.status_code == 200
    assert isinstance(data, list)


def test_register():
    response, data = post("/api/auth/register", {"email": "", "password": ""})
    assert response.status_code == 400


def test_login():
    response, data = post("/api/auth/login", {"email": "", "password": ""})
    assert response.status_code == 400


def test_logout():
    response = get("/api/auth/logout", False)
    assert response.status_code == 401


def test_static_routes():
    for route in ["/docs/", "/_static/jquery.js"]:
        response = get(route, False)
        assert response.status_code == 200
