import base64
import contextlib
import hashlib
import hmac
import logging
import typing as t

import boto3

import mantik.mlflow_server.tokens.cognito.client as _client
import mantik.mlflow_server.tokens.cognito.credentials as _credentials
import mantik.mlflow_server.tokens.cognito.exceptions as exceptions

logger = logging.getLogger(__name__)


@contextlib.contextmanager
def cognito_auth_response(
    credentials: _credentials.Credentials,
    cognito: t.Optional[_client.Properties] = None,
    client: t.Optional[t.Type[boto3.client]] = None,
) -> t.Dict:
    """Get the required tokens from the Cognito API using given auth flow.

    Raises
    ------
    AuthenticationFailedException
        If the authentication failed for a known reason.

    """
    if cognito is None:
        cognito = _client.Properties.from_env()

    if client is None:
        client = boto3.client("cognito-idp", region_name=cognito.region)

    yield _get_auth_response(
        client=client,
        credentials=credentials,
        cognito=cognito,
    )

    client.close()


def _get_auth_response(
    client: boto3.client,
    credentials: _credentials.Credentials,
    cognito: _client.Properties,
) -> t.Dict:
    auth_parameters = _add_secret_hash_to_auth_parameters(
        auth_parameters=credentials.to_auth_parameters(),
        credentials=credentials,
        cognito=cognito,
    )
    try:
        return client.initiate_auth(
            ClientId=cognito.app_client_id,
            AuthFlow=credentials.auth_flow,
            AuthParameters=auth_parameters,
        )
    except client.exceptions.UserNotFoundException as e:
        message = e.response["Error"]["Message"]
        if "user does not exist" in message.lower():
            raise exceptions.AuthenticationFailedException(message)
        raise e
    except client.exceptions.NotAuthorizedException as e:
        message = e.response["Error"]["Message"]
        if "incorrect username or password" in message.lower():
            raise exceptions.AuthenticationFailedException(message)
        elif "refresh token has expired" in message.lower():
            raise exceptions.AuthenticationFailedException(
                exceptions.REFRESH_TOKEN_EXPIRED_ERROR_MESSAGE
            )
        elif "invalid refresh token" in message.lower():
            raise exceptions.AuthenticationFailedException(
                exceptions.REFRESH_TOKEN_INVALID_ERROR_MESSAGE
            )
        elif "refresh token has different client" in message.lower():
            raise exceptions.AuthenticationFailedException(
                exceptions.REFRESH_TOKEN_INVALID_ERROR_MESSAGE
            )
        raise e


def _add_secret_hash_to_auth_parameters(
    auth_parameters: t.Dict[str, str],
    credentials: _credentials.Credentials,
    cognito: _client.Properties,
) -> t.Dict:
    secret_hash = _create_secret_hash(
        credentials=credentials,
        cognito=cognito,
    )
    return {
        **auth_parameters,
        "SECRET_HASH": secret_hash,
    }


def _create_secret_hash(
    credentials: _credentials.Credentials,
    cognito: _client.Properties,
) -> str:
    """Create a secret hash for secret-protected clients.

    Notes
    -----
    See
    https://aws.amazon.com/premiumsupport/knowledge-center/cognito-unable-to-verify-secret-hash/  # noqa

    """
    message = bytes(credentials.username + cognito.app_client_id, "utf-8")
    key = bytes(cognito.app_client_secret, "utf-8")
    hmac_key = hmac.new(key, message, digestmod=hashlib.sha256).digest()
    hashed = base64.b64encode(hmac_key).decode()
    return hashed
