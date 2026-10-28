import pytest

from backend.api.auth import get_auth_repository
from backend.core.weak_auth import token_hash
from backend.main import app
from backend.storage.sqlite import SQLiteRepository


@pytest.fixture()
def auth_client(client, tmp_path):
    repo = SQLiteRepository.from_path(tmp_path / "auth.sqlite")
    app.dependency_overrides[get_auth_repository] = lambda: repo
    yield client, repo
    app.dependency_overrides.pop(get_auth_repository, None)


@pytest.mark.parametrize(
    ("email", "normalized_email"),
    [
        ("Professor@BNBU.edu.cn", "professor@bnbu.edu.cn"),
        (" Student@MAIL.BNBU.EDU.CN ", "student@mail.bnbu.edu.cn"),
    ],
)
def test_bnbu_users_can_register_login_and_read_me(auth_client, email, normalized_email):
    client, repo = auth_client
    payload = {
        "email": email,
        "password": "correct-horse",
        "confirm_password": "correct-horse",
    }

    register = client.post("/api/auth/register", json=payload)
    assert register.status_code == 200
    assert register.json() == {
        "status": "success",
        "email": normalized_email,
        "role": "teacher",
    }
    user = repo.get_user_by_email(normalized_email)
    assert user is not None
    assert "correct-horse" not in user["password_hash"]

    login = client.post(
        "/api/auth/login",
        json={"email": email, "password": "correct-horse"},
    )
    assert login.status_code == 200
    login_body = login.json()
    token = login_body["token"]
    assert token
    assert normalized_email not in token
    assert repo.get_session_by_token_hash(token_hash(token))["token_hash"] != token

    me = client.get("/api/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert me.status_code == 200
    assert me.json() == {"email": normalized_email, "role": "teacher"}


@pytest.mark.parametrize(
    "email",
    [
        "person@example.com",
        "person@bnbu.edu.cn.example.com",
        "person@mail.bnbu.edu.cn.example.com",
        "person@other.bnbu.edu.cn",
        "person@notmail.bnbu.edu.cn",
    ],
)
def test_unknown_domain_is_rejected(auth_client, email):
    client, _repo = auth_client

    response = client.post(
        "/api/auth/register",
        json={
            "email": email,
            "password": "correct-horse",
            "confirm_password": "correct-horse",
        },
    )

    assert response.status_code == 400
    assert response.json()["error"]["code"] == "unknown_email_domain"

    login = client.post(
        "/api/auth/login",
        json={"email": email, "password": "correct-horse"},
    )
    assert login.status_code == 400
    assert login.json()["error"]["code"] == "unknown_email_domain"


def test_missing_and_invalid_bearer_token_are_rejected(auth_client):
    client, _repo = auth_client

    missing = client.get("/api/auth/me")
    invalid = client.get("/api/auth/me", headers={"Authorization": "Bearer nope"})

    assert missing.status_code == 401
    assert missing.json()["error"]["code"] == "unauthorized"
    assert invalid.status_code == 401
    assert invalid.json()["error"]["code"] == "unauthorized"
