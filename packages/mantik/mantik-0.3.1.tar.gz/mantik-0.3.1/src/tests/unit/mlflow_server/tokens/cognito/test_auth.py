import typing as t

import pytest

import mantik.mlflow_server.tokens.cognito as _cognito
import mantik.mlflow_server.tokens.cognito._auth as _auth
import mantik.testing as testing

GENERATED_SECRET_HASH = "G/xu9YVG49BHbE9jLXEIkY6bHFSev/r1t0zvOBpK47M="


@pytest.fixture(autouse=True)
def cognito_patcher():
    with testing.cognito.CognitoClientPatcher() as patcher:
        yield patcher
        patcher.assert_no_pending_responses()


@pytest.fixture()
def cognito() -> _cognito.client.Properties:
    return _cognito.client.Properties(
        region="test-region",
        user_pool_id="test-user-pool-id",
        app_client_id="test-app-client-id",
        app_client_secret="test-app-client-secret",
    )


@pytest.mark.parametrize(
    (
        "cognito_response",
        "expected",
    ),
    [
        (
            "cognito_auth_response",
            None,
        ),
        (
            "cognito_user_not_found_response",
            _cognito.exceptions.AuthenticationFailedException(),
        ),
        (
            "cognito_incorrect_login_credentials_response",
            _cognito.exceptions.AuthenticationFailedException(),
        ),
    ],
)
def test_cognito_auth_response_get_token(
    cognito_patcher,
    cognito,
    request,
    cognito_response,
    expected,
):
    credentials = _cognito.credentials.CreateTokenCredentials(
        username="test-user",
        password="test-password",
    )

    fake_response = request.getfixturevalue(cognito_response)
    error_code, error_message = _create_error_code_and_message(fake_response)
    cognito_patcher.patch_initiate_auth_get_token(
        client_id=cognito.app_client_id,
        user_name=credentials.username,
        password=credentials.password,
        secret_hash=GENERATED_SECRET_HASH,
        response=fake_response,
        error_code=error_code,
        error_message=error_message,
    )

    _call_method_and_assert_expected(
        credentials=credentials,
        cognito=cognito,
        cognito_patcher=cognito_patcher,
        expected=expected or fake_response,
    )


@pytest.mark.parametrize(
    (
        "cognito_response",
        "expected",
    ),
    [
        (
            "cognito_refresh_response",
            None,
        ),
        (
            "cognito_refresh_token_expired_response",
            _cognito.exceptions.AuthenticationFailedException(),
        ),
    ],
)
def test_cognito_auth_response_refresh_token(
    cognito_patcher,
    cognito,
    request,
    cognito_response,
    expected,
):
    credentials = _cognito.credentials.RefreshTokenCredentials(
        username="test-user",
        refresh_token="test-refresh-token",
    )

    fake_response = request.getfixturevalue(cognito_response)
    error_code, error_message = _create_error_code_and_message(fake_response)
    cognito_patcher.patch_initiate_auth_refresh_token(
        client_id=cognito.app_client_id,
        refresh_token=credentials.refresh_token,
        secret_hash=GENERATED_SECRET_HASH,
        response=fake_response,
        error_code=error_code,
        error_message=error_message,
    )

    _call_method_and_assert_expected(
        credentials=credentials,
        cognito=cognito,
        cognito_patcher=cognito_patcher,
        expected=expected or fake_response,
    )


def _create_error_code_and_message(fake_response: t.Dict) -> t.Tuple[str, str]:
    error_code = None
    error_message = None
    if "Error" in fake_response:
        error_code = fake_response["Error"]["Code"]
        error_message = fake_response["Error"]["Message"]
    return error_code, error_message


def _call_method_and_assert_expected(
    credentials: _cognito.credentials.Credentials,
    cognito: _cognito.client.Properties,
    cognito_patcher: testing.cognito.CognitoClientPatcher,
    expected: t.Any,
) -> None:
    with testing.contexts.expect_raise_if_exception(expected):
        with _auth.cognito_auth_response(
            credentials=credentials,
            cognito=cognito,
            client=cognito_patcher.client,
        ) as response:
            result = response

        assert result == expected
