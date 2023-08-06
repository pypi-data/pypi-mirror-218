import functools
import typing as t

import mantik.mlflow_server.tokens.cognito._auth as _auth
import mantik.mlflow_server.tokens.cognito.client as _client
import mantik.mlflow_server.tokens.cognito.credentials as _credentials
import mantik.mlflow_server.tokens.cognito.tokens as _tokens


@functools.singledispatch
def get_tokens(
    credentials: _credentials.Credentials,
    cognito: t.Optional[_client.Properties] = None,
) -> _tokens.Tokens:
    """Get the required tokens from the Cognito API."""
    return NotImplemented


@get_tokens.register
def _get_tokens(
    credentials: _credentials.CreateTokenCredentials,
    cognito: t.Optional[_client.Properties] = None,
) -> _tokens.Tokens:
    response = _get_tokens_from_cognito(
        credentials=credentials,
        cognito=cognito,
    )
    return _tokens.Tokens.from_json_response(response)


@get_tokens.register
def _refresh_tokens(
    credentials: _credentials.RefreshTokenCredentials,
    cognito: t.Optional[_client.Properties] = None,
) -> _tokens.Tokens:
    response = _get_tokens_from_cognito(
        credentials=credentials,
        cognito=cognito,
    )
    return _tokens.Tokens.from_json_response(
        response,
        refresh_token=credentials.refresh_token,
    )


def _get_tokens_from_cognito(
    credentials: _credentials.Credentials,
    cognito: t.Optional[_client.Properties] = None,
) -> t.Dict:
    with _auth.cognito_auth_response(
        credentials=credentials,
        cognito=cognito,
    ) as response:
        return response
