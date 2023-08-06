import logging
import os
import typing as t
import uuid

import requests

import mantik.utils.mantik_api.credentials as credentials
import mantik.utils.mantik_api.data_repository as data_repository

MANTIK_API_URL_ENV_VAR = "MANTIK_API_URL"
MANTIK_API_URL = "https://api.cloud.mantik.ai"

_TOKENS_API_PATH_PREFIX = "/mantik-api/mantik/tokens"
MANTIK_API_CREATE_TOKEN_API_PATH = f"{_TOKENS_API_PATH_PREFIX}/create"
MANTIK_API_REFRESH_TOKEN_API_PATH = f"{_TOKENS_API_PATH_PREFIX}/refresh"

logger = logging.getLogger(__name__)


def create_data_repository(
    add_data_repository: data_repository.AddDataRepositoryModel,
    project_id: uuid.UUID,
    token: str,
):
    data = add_data_repository.to_dict()
    endpoint = f"/mantik-api/projects/{str(project_id)}/data"
    response = _send_request_to_mantik_api("POST", data, endpoint, token)
    logger.info(
        f'A new data repository with id: {response.json()["dataRepositoryId"]} '
        f"and name: {add_data_repository.data_repository_name} at "
        f"{add_data_repository.uri} has been created"
    )


def delete_data_repository(
    project_id: uuid.UUID,
    data_repository_id: uuid.UUID,
    token: str,
):
    data = {}
    endpoint = (
        f"/mantik-api/projects/{str(project_id)}/data/{str(data_repository_id)}"
    )
    _send_request_to_mantik_api("DELETE", data, endpoint, token)
    logger.info(
        f"Data repository with id: {data_repository_id} has been deleted"
    )


def get_data_repositories(
    project_id: uuid.UUID,
    token: str,
) -> t.List[t.Dict]:
    endpoint = f"/mantik-api/projects/{str(project_id)}/data"
    response = _send_request_to_mantik_api("GET", {}, endpoint, token)
    return response.json()["dataRepositories"]


def create_tokens(
    access_credentials: t.Optional[credentials.Credentials] = None,
) -> t.Dict:
    """Get tokens from the Mantik API."""
    if access_credentials is None:
        access_credentials = credentials.Credentials.from_env()
    response = _send_request_to_mantik_api(
        "POST", access_credentials.to_dict(), MANTIK_API_CREATE_TOKEN_API_PATH
    )
    return response.json()


def refresh_tokens(
    refresh_token: str,
    access_credentials: t.Optional[credentials.Credentials] = None,
) -> t.Dict:
    """Get tokens from the Mantik API."""
    if access_credentials is None:
        access_credentials = credentials.Credentials.from_env()
    data = {
        **access_credentials.to_dict(include_password=False),
        "refresh_token": refresh_token,
    }
    response = _send_request_to_mantik_api(
        "POST", data, MANTIK_API_REFRESH_TOKEN_API_PATH
    )
    return response.json()


def _send_request_to_mantik_api(
    method: str,
    data: dict,
    url_endpoint: str,
    token: t.Optional[str] = None,
) -> requests.Response:
    base_url = os.environ.get(MANTIK_API_URL_ENV_VAR, MANTIK_API_URL)
    url = _clean_double_slashes(f"{base_url}{url_endpoint}")
    header = (
        {
            "Authorization": f"Bearer {token}",
            "Accept": "application/json",
        }
        if token
        else None
    )
    request = {"url": url, "json": data, "headers": header}
    try:
        response = requests.request(method, **request)
        response.raise_for_status()
    except requests.HTTPError:
        logger.exception(
            "Call to Mantik API %s with data %s failed",
            url,
            data,
            exc_info=True,
        )
        raise
    else:
        return response


def _clean_double_slashes(url: str) -> str:
    scheme, rest = url.split("://", 1)
    clean_rest = rest.replace("//", "/")
    clean_url = f"{scheme}://{clean_rest}"
    return clean_url
