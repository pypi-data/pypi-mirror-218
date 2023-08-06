import datetime
import typing as t

import pytest
import requests

import mantik.mlflow_server.flask.api.tokens as tokens
import mantik.mlflow_server.tokens.cognito.client as _client
import mantik.testing as testing
import mantik.utils.env as env

REQUIRED_ENV_VARS = {
    _client.COGNITO_APP_CLIENT_ID_ENV_VAR: "test-client-id",
    _client.COGNITO_APP_CLIENT_SECRET_ENV_VAR: "test-client-secret",
    _client.COGNITO_REGION_ENV_VAR: "test-region",
    _client.COGNITO_USER_POOL_ID_ENV_VAR: "test-user-pool-id",
}


@pytest.mark.parametrize(
    (
        "cognito_response",
        "expected_status_code",
        "expected_payload",
        "expected_message",
    ),
    [
        (
            "cognito_auth_response",
            201,
            {
                "AccessToken": "test-access-token",
                "RefreshToken": "test-refresh-token",
                "ExpiresAt": datetime.datetime(
                    2022, 5, 24, 9, 40, 19, tzinfo=datetime.timezone.utc
                ).isoformat(),
            },
            None,
        ),
        (
            "cognito_user_not_found_response",
            401,
            None,
            "user does not exist",
        ),
        (
            "cognito_incorrect_login_credentials_response",
            401,
            None,
            "incorrect username or password",
        ),
    ],
)
def test_create_token(
    monkeypatch,
    client,
    request,
    cognito_response,
    expected_status_code,
    expected_payload,
    expected_message,
):
    _patch_boto_client(
        request=request,
        monkeypatch=monkeypatch,
        fixture_name=cognito_response,
    )

    data = {
        "username": "test-user",
        "password": "test-password",
    }

    with env.env_vars_set(REQUIRED_ENV_VARS):
        response = client.post(tokens.CREATE_TOKEN_API_PATH, json=data)

    _expect_correct_response(
        response=response,
        expected_status_code=expected_status_code,
        expected_payload=expected_payload,
        expected_message=expected_message,
    )


@pytest.mark.parametrize(
    (
        "cognito_response",
        "expected_status_code",
        "expected_payload",
        "expected_message",
    ),
    [
        (
            "cognito_refresh_response",
            201,
            {
                "AccessToken": "test-refreshed-access-token",
                "ExpiresAt": datetime.datetime(
                    2022, 6, 7, 14, 21, 6, tzinfo=datetime.timezone.utc
                ).isoformat(),
            },
            None,
        ),
        (
            "cognito_refresh_token_expired_response",
            401,
            None,
            "refresh token has expired",
        ),
        (
            "cognito_refresh_token_invalid_response",
            401,
            None,
            "refresh token is invalid",
        ),
        (
            "cognito_different_client_response",
            401,
            None,
            "refresh token is invalid",
        ),
    ],
)
def test_refresh_token(
    monkeypatch,
    client,
    request,
    cognito_response,
    expected_status_code,
    expected_payload,
    expected_message,
):
    _patch_boto_client(
        request=request,
        monkeypatch=monkeypatch,
        fixture_name=cognito_response,
    )

    data = {
        "refresh_token": "test-refresh-token",
        "username": "test-user",
    }

    with env.env_vars_set(REQUIRED_ENV_VARS):
        response = client.post(tokens.REFRESH_TOKEN_API_PATH, json=data)

    _expect_correct_response(
        response=response,
        expected_status_code=expected_status_code,
        expected_payload=expected_payload,
        expected_message=expected_message,
    )


def _patch_boto_client(request, monkeypatch, fixture_name: str) -> None:
    json_response = request.getfixturevalue(fixture_name)
    testing.cognito.patch_boto_client(monkeypatch, json_response=json_response)


def _expect_correct_response(
    response: requests.Response,
    expected_status_code: int,
    expected_payload: t.Optional[t.Dict],
    expected_message: t.Optional[str],
) -> None:
    assert response.status_code == expected_status_code
    if expected_payload is not None:
        assert response.json == expected_payload
    if expected_message is not None:
        assert expected_message.lower() in response.text.lower()
