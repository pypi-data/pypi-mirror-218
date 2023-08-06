import contextlib
import datetime
import logging
import os
import pathlib
import typing as t

import pytest
import requests_mock

import mantik.authentication.auth as track
import mantik.unicore.config.environment
import mantik.utils as utils
import mantik.utils.mantik_api.client as mantik_api
import mantik.utils.mantik_api.credentials as _credentials
import mantik.utils.mantik_api.data_repository as data_repository


@pytest.fixture()
def mlflow_tracking_uri() -> str:
    return "https://test-uri.com"


@pytest.fixture()
def required_env_vars(mlflow_tracking_uri) -> t.Dict[str, str]:
    return {
        _credentials._MANTIK_USERNAME_ENV_VAR: "test-user",
        _credentials._MANTIK_PASSWORD_ENV_VAR: "test-password",
        utils.mlflow.TRACKING_URI_ENV_VAR: mlflow_tracking_uri,
        # If the env vars for MLflow user/password are set, these are
        # prioritized by MLflow over the token. This leads to an
        # `Unauthorized` error.
        utils.mlflow.TRACKING_USERNAME_ENV_VAR: "must-be-unset",
        utils.mlflow.TRACKING_PASSWORD_ENV_VAR: "must-be-unset",
    }


@pytest.fixture()
def token_expiration_date() -> datetime.datetime:
    return datetime.datetime(2022, 1, 1)


@pytest.fixture()
def tmp_dir_as_test_mantik_folder(tmp_path):
    track._MANTIK_FOLDER = pathlib.Path(tmp_path)
    track._MANTIK_TOKEN_FILE = track._MANTIK_FOLDER / "tokens.json"
    return tmp_path


def pytest_configure(config):
    """Remove all MLFLOW_ related environment variables before running any
    test to simplify tests setup."""
    for env in mantik.unicore.config.environment._get_mlflow_env_vars():
        del os.environ[env]


@pytest.fixture
def env_vars_set():
    @contextlib.contextmanager
    def wrapped(env_vars: t.Dict[str, t.Any]):
        for key, value in env_vars.items():
            os.environ[key] = value
        yield
        for key in env_vars:
            try:
                os.environ.pop(key)
            except KeyError:
                pass

    return wrapped


@pytest.fixture
def expect_raise_if_exception() -> (
    t.Callable[[t.Any], contextlib.AbstractContextManager]
):
    def expect_can_be_error(
        expected: t.Any,
    ) -> contextlib.AbstractContextManager:
        return (
            pytest.raises(type(expected))
            if isinstance(expected, Exception)
            else contextlib.nullcontext()
        )

    return expect_can_be_error


@pytest.fixture
def mock_mantik_api_request(env_vars_set, expect_raise_if_exception):
    @contextlib.contextmanager
    def wrapped(
        method: str,
        end_point: str,
        status_code: int,
        json_response: dict,
        expected_error: t.Optional[Exception],
    ) -> None:
        base_url = "https://test.com"
        env_vars = {mantik_api.MANTIK_API_URL_ENV_VAR: base_url}
        with requests_mock.Mocker() as m, env_vars_set(
            env_vars
        ), expect_raise_if_exception(expected_error) as e:
            m.register_uri(
                method=method,
                url=f"{base_url}{end_point}",
                status_code=status_code,
                json=json_response,
            )
            yield e

    return wrapped


@pytest.fixture
def add_data_repository():
    return data_repository.AddDataRepositoryModel(
        uri="test_uri",
        data_repository_name="test_name",
        access_token=None,
        description="test_description",
    )


@pytest.fixture
def info_caplog(caplog):
    caplog.set_level(logging.INFO)
    yield caplog
