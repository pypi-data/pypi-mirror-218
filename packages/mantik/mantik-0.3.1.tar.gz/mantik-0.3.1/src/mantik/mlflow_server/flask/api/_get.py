import functools

import mantik.mlflow_server.flask.api._exceptions as _exceptions
import mantik.mlflow_server.flask.api.models as models
import mantik.mlflow_server.tokens.cognito as _cognito


@functools.singledispatch
def get_tokens(
    request: models.requests.TokenRequest,
) -> models.responses.TokenResponse:
    """Get the tokens from the API.

    Raises
    ------
    AuthenticationFailedException
        If the authentication has failed.

    """
    return NotImplemented


@get_tokens.register
def _get_tokens(
    request: models.requests.CreateTokenRequest,
) -> models.responses.CreateTokenResponse:
    tokens = _get_tokens_from_api(request)
    return models.responses.CreateTokenResponse.from_cognito_tokens(tokens)


@get_tokens.register
def _refresh_tokens(
    request: models.requests.RefreshTokenRequest,
) -> models.responses.RefreshTokenResponse:
    tokens = _get_tokens_from_api(request)
    return models.responses.RefreshTokenResponse.from_cognito_tokens(tokens)


def _get_tokens_from_api(
    request: models.requests.TokenRequest,
) -> _cognito.tokens.Tokens:
    credentials = request.to_cognito_credentials()
    try:
        return _cognito.api.get_tokens(credentials)
    except _cognito.exceptions.AuthenticationFailedException as e:
        raise _exceptions.AuthenticationFailedException(str(e))
