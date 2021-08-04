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
        url,
        data=flask.json.dumps(payload),
        content_type="application/json",
    )
    if not get_data:
        return response
    data = flask.json.loads(response.get_data(as_text=True))
    return (response, data)


def delete(client, url):
    return client.delete(url)


def test_widgets(client):
    response, data = get(client, "/api/widgets")

    assert response.status_code == 200
    assert isinstance(data, list)
    assert len(data)
    assert "name" in data[0] and "path" in data[0]


def test_field_validation(client):
    response, data = get(client, "/api/fields/Equation?value=x^2")
    assert response.status_code == 200
    assert data["valid"]

    response, data = get(client, "/api/fields/Equation?value=/")
    assert response.status_code == 400

    response, data = get(client, "/api/fields/Eequation?value=/")
    assert response.status_code == 404

    response, data = get(client, "/api/fields/Equation")
    assert response.status_code == 400


def test_widget(client):
    response, data = get(client, "/api/widgets/Equation")
    assert response.status_code == 200
    assert "fields" in data and "template" in data

    response, data = get(client, "/api/widgets/Eequation")
    assert response.status_code == 404


def test_widget_validation(client):
    response, data = get(client, "/api/widgets/Equation?equation=x^2")
    assert response.status_code == 200
    assert data["solution"] == "[Eq(x, 0)]"

    response, data = post(client, "/api/widgets/LinearEquation", {"one_step": "1"})
    assert data["equation"]
    assert response.status_code == 200

    response, data = get(client, "/api/widgets/Equation?equation=sin(")
    assert response.status_code == 400

    response, data = get(client, "/api/widgets/Equation?x=x")
    assert response.status_code == 400


def test_list_slideshows(client, mock_mongo):
    response, data = get(client, "/api/slideshows")
    assert response.status_code == 200

    assert isinstance(data[0]["url"], str)


def test_retrieve_slideshow(client, mock_mongo):
    slideshow = db.slideshows.find_one({})
    assert slideshow["_id"]
    response, data = get(client, f"/api/slideshows/{slideshow['url']}")
    assert response.status_code == 200
    assert isinstance(data, list)


def test_save_slideshow(client, mock_mongo):
    slideshow = db.slideshows.find_one({})

    response, data = get(client, "/api/auth/login")
    assert response.status_code == 200
    assert not data["is_authenticated"]
    response = post(
        client,
        f"/api/slideshows/{slideshow['url']}",
        {"key": "1", "patch": {"title": "Hello"}},
        False,
    )
    assert response.status_code == 401

    response, data = post(
        client, "/api/auth/login", {"email": "test@test.com", "password": "testtest"}
    )
    assert response.status_code == 200
    response, data = post(
        client,
        f"/api/slideshows/{slideshow['url']}",
        {"key": "1", "patch": {"title": "Hello"}},
    )
    assert response.status_code == 200
    response, data = post(
        client,
        f"/api/slideshows/{slideshow['url']}",
        {"title": "Hello"},
    )
    assert response.status_code == 200
    assert data["title"] == "Hello"
    db.slideshows.delete_many({})
    response, data = post(
        client,
        f"/api/slideshows/{slideshow['url']}",
        {"key": "1", "patch": {"title": "Hello"}},
    )
    assert response.status_code == 200

    count = db.slideshows.count_documents({})
    response, data = post(
        client,
        "/api/slideshows/",
        {"title": "Hello"},
    )
    assert response.status_code == 200
    assert db.slideshows.count_documents({}) == count + 1


def test_delete_slideshow(client, mock_mongo):
    slideshow = db.slideshows.find_one({})

    response, data = get(client, "/api/auth/login")
    assert response.status_code == 200
    assert not data["is_authenticated"]

    response = delete(client, f"/api/slideshows/{slideshow['url']}")
    assert response.status_code == 401

    response, data = post(
        client, "/api/auth/login", {"email": "test@test.com", "password": "testtest"}
    )
    assert response.status_code == 200

    count = db.slideshows.count_documents({})
    response = delete(client, f"/api/slideshows/{slideshow['url']}")
    assert response.status_code == 204
    assert db.slideshows.count_documents({}) == count - 1


# def test_register(client, mock_mongo):
#     response, data = post(client, "/api/auth/register", {"email": "", "password": ""})
#     assert response.status_code == 400
#
#     response, data = post(
#         client, "/api/auth/register", {"email": "test@test.com", "password": "testtest"}
#     )
#     assert response.status_code == 400
#
#     response, data = post(
#         client,
#         "/api/auth/register",
#         {"email": "test2@test.com", "password": "testtest"},
#     )
#     assert response.status_code == 200


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


def test_tests(client):
    response, data = get(client, "/api/tests")
    assert response.status_code == 200
    assert isinstance(data, dict)


def test_delete_test_user(client, mock_mongo):
    response = post(
        client,
        "/api/auth/login",
        {"email": "test@test.com", "password": "testtest"},
        get_data=False,
    )
    assert response.status_code == 200
    count = db.collections.users.count_documents({})
    response = delete(client, "/api/tests/user")
    assert response.status_code == 204
    assert db.collections.users.count_documents({}) == count - 1

    # response = post(
    #     client,
    #     "/api/auth/register",
    #     {"email": "test@test.com", "password": "testtest"},
    #     get_data=False,
    # )
    # assert response.status_code == 200
    # assert db.collections.users.count_documents({}) == count


def test_static_routes(client):
    for route in ["/docs/", "/_static/jquery.js", "/slideshow_builder", "/favicon.ico"]:
        response = get(client, route, False)
        assert response.status_code == 200
