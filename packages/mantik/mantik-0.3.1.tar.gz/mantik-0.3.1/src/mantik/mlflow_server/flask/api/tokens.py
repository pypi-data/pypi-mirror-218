import typing as t

import flask

import mantik.mlflow_server.flask.api._exceptions as _exceptions
import mantik.mlflow_server.flask.api._get as _get
import mantik.mlflow_server.flask.api.models as models
import mantik.mlflow_server.flask.app as _app
import mantik.mlflow_server.flask.skip as skip

app = _app.app

_API_PATH_PREFIX = "/api/mantik"
_TOKENS_API_PATH_PREFIX = f"{_API_PATH_PREFIX}/tokens"

CREATE_TOKEN_API_PATH = f"{_TOKENS_API_PATH_PREFIX}/create"
REFRESH_TOKEN_API_PATH = f"{_TOKENS_API_PATH_PREFIX}/refresh"


@app.route(CREATE_TOKEN_API_PATH, methods=["POST"])
@skip.skip_authentication
def create_token() -> flask.Response:
    """Create a token from an AWS Cognito User Pool."""
    return _get_token(
        request=flask.request, request_type=models.requests.CreateTokenRequest
    )


@app.route(REFRESH_TOKEN_API_PATH, methods=["POST"])
@skip.skip_authentication
def refresh_token() -> flask.Response:
    """Refresh a token from an AWS Cognito User Pool."""
    return _get_token(
        request=flask.request, request_type=models.requests.RefreshTokenRequest
    )


def _get_token(
    request: flask.Request, request_type: t.Type[models.requests.TokenRequest]
) -> flask.Response:
    data = _parse_request_data(request=request, request_type=request_type)
    try:
        response = _get.get_tokens(data)
    except _exceptions.AuthenticationFailedException as e:
        return flask.make_response(str(e), 401)
    else:
        return _to_json_response(response)


def _parse_request_data(
    request: flask.Request, request_type: t.Type[models.requests.TokenRequest]
) -> models.requests.TokenRequest:
    data = request.get_json()
    return request_type.parse_obj(data)


def _to_json_response(
    response: models.responses.TokenResponse,
) -> flask.Response:
    return flask.make_response(flask.jsonify(response.to_dict()), 201)
