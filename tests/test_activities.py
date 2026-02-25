from urllib.parse import quote
from src.app import activities


def test_get_activities(client, activities_reset):
    # Arrange: client fixture ready

    # Act
    resp = client.get("/activities")

    # Assert
    assert resp.status_code == 200
    assert isinstance(resp.json(), dict)


def test_signup_success(client, activities_reset):
    # Arrange
    activity_path = quote("Chess Club")  # "Chess%20Club"
    email = "new@mergington.edu"

    # Act
    resp = client.post(f"/activities/{activity_path}/signup", params={"email": email})

    # Assert
    assert resp.status_code == 200
    assert email in activities["Chess Club"]["participants"]


def test_duplicate_signup(client, activities_reset):
    # Arrange
    activity_path = quote("Chess Club")
    email = "dup@mergington.edu"

    # Act
    resp1 = client.post(f"/activities/{activity_path}/signup", params={"email": email})
    resp2 = client.post(f"/activities/{activity_path}/signup", params={"email": email})

    # Assert
    assert resp1.status_code == 200
    assert resp2.status_code == 400


def test_signup_nonexistent(client, activities_reset):
    # Arrange
    email = "x@x.com"

    # Act
    resp = client.post("/activities/NoSuchActivity/signup", params={"email": email})

    # Assert
    assert resp.status_code == 404


def test_unregister_success(client, activities_reset):
    # Arrange
    activity_path = quote("Chess Club")
    email = "toremove@mergington.edu"

    # Act: sign up then unregister
    resp_signup = client.post(f"/activities/{activity_path}/signup", params={"email": email})
    resp_unreg = client.delete(f"/activities/{activity_path}/signup", params={"email": email})

    # Assert
    assert resp_signup.status_code == 200
    assert resp_unreg.status_code == 200
    assert email not in activities["Chess Club"]["participants"]


def test_unregister_not_registered(client, activities_reset):
    # Arrange
    activity_path = quote("Chess Club")
    email = "notregistered@mergington.edu"

    # Act
    resp = client.delete(f"/activities/{activity_path}/signup", params={"email": email})

    # Assert
    assert resp.status_code == 400


def test_unregister_nonexistent_activity(client, activities_reset):
    # Arrange
    email = "x@x.com"

    # Act
    resp = client.delete("/activities/NoSuchActivity/signup", params={"email": email})

    # Assert
    assert resp.status_code == 404
