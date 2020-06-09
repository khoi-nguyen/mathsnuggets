import flask
import pytest

from app import app
from mathsnuggets.core import db


@pytest.fixture
def mock_mongo(mongodb, monkeypatch):
    monkeypatch.setattr(db, "collections", mongodb)
    monkeypatch.setattr(db, "slideshows", mongodb.slideshows)


@pytest.fixture
def client():
    with app.test_client() as client:
        yield client


def test_mockmongo(mock_mongo):
    assert "users" in db.collections.list_collection_names()
    user = db.collections.users.find_one({"email": "test@test.com"})
    assert user


def get(client, url, get_data=True):
    response = client.get(url)
    if not get_data:
        return response
    data = flask.json.loads(response.get_data(as_text=True))
    return (response, data)


def post(client, url, payload, get_data=True):
    response = client.post(
        url, data=flask.json.dumps(payload), content_type="application/json",
    )
    if not get_data:
        return response
    data = flask.json.loads(response.get_data(as_text=True))
    return (response, data)


def test_widgets(client):
    response, data = get(client, "/api/widgets")

    assert response.status_code == 200
    assert isinstance(data, list)
    assert len(data)
    assert "name" in data[0] and "path" in data[0]


def test_field_validation(client):
    response, data = post(
        client, "/api/fields/Equation", {"name": "eq", "value": "x^2"}
    )
    assert response.status_code == 200
    assert data["valid"]

    response, data = post(client, "/api/fields/Equation", {"name": "eq", "value": "/"})
    assert response.status_code == 400

    response, data = post(client, "/api/fields/Eequation", {"name": "eq", "value": "/"})
    assert response.status_code == 404

    response, data = post(client, "/api/fields/Equation", {"name": "eq"})
    assert response.status_code == 400


def test_widget(client):
    response, data = get(client, "/api/widgets/Equation")
    assert response.status_code == 200
    assert isinstance(data, list)

    response, data = get(client, "/api/widgets/Eequation")
    assert response.status_code == 404


def test_widget_validation(client):
    response, data = post(client, "/api/widgets/Equation", {"equation": "x^2"})
    assert response.status_code == 200
    assert data["solution"]["value"] == "FiniteSet(0)"

    response, data = post(
        client, "/api/widgets/LinearEquation/generator", {"one_step": "1"}
    )
    assert data["equation"]["value"]
    assert response.status_code == 200

    response, data = post(client, "/api/widgets/Equation", {"equation": "sin("})
    assert response.status_code == 400

    response, data = post(client, "/api/widgets/Equation", {"x": "x"})
    assert response.status_code == 400


def test_retrieve_slideshow(client, mock_mongo):
    assert db.slideshows.count_documents({})
    response, data = get(client, "/api/slideshows")
    assert response.status_code == 200
    assert isinstance(data, list)


def test_save_slideshow(client, mock_mongo):
    response = post(
        client, "/api/slideshows/save", {"key": "1", "patch": {"title": "Hello"}}, False
    )
    assert response.status_code == 401

    response, data = post(
        client, "/api/auth/login", {"email": "test@test.com", "password": "testtest"}
    )
    assert response.status_code == 200
    response, data = post(
        client, "/api/slideshows/save", {"key": "1", "patch": {"title": "Hello"}}
    )
    assert response.status_code == 200
    db.slideshows.delete_many({})
    response, data = post(
        client, "/api/slideshows/save", {"key": "1", "patch": {"title": "Hello"}}
    )
    assert response.status_code == 200


def test_register(client, mock_mongo):
    response, data = post(client, "/api/auth/register", {"email": "", "password": ""})
    assert response.status_code == 400

    response, data = post(
        client, "/api/auth/register", {"email": "test@test.com", "password": "testtest"}
    )
    assert response.status_code == 400

    response, data = post(
        client,
        "/api/auth/register",
        {"email": "test2@test.com", "password": "testtest"},
    )
    assert response.status_code == 200


def test_login_logout(client, mock_mongo):
    response, data = get(client, "/api/auth/login")
    assert response.status_code == 200
    assert not data["is_authenticated"]

    response, data = post(client, "/api/auth/login", {"email": "", "password": ""})
    assert response.status_code == 400

    response, data = post(
        client, "/api/auth/login", {"email": "test@test.com", "password": "hellohello"}
    )
    assert response.status_code == 400

    response, data = post(
        client, "/api/auth/login", {"email": "test@test.com", "password": "testtest"}
    )
    assert response.status_code == 200
    response, data = get(client, "/api/auth/login")
    assert response.status_code == 200
    assert data["is_authenticated"]
    response, data = get(client, "/api/auth/logout")
    assert response.status_code == 200


def test_logout(client):
    response = get(client, "/api/auth/logout", False)
    assert response.status_code == 401


def test_static_routes(client):
    for route in ["/docs/", "/_static/jquery.js", "/slideshow_builder"]:
        response = get(client, route, False)
        assert response.status_code == 200
