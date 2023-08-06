import os
import pathlib

import pytest

import mantik.utils as utils


@pytest.fixture(scope="session")
def mlproject_path() -> pathlib.Path:
    return (
        pathlib.Path(__file__).parent
        / "../../../../../src/tests/resources/test-project"
    )


@pytest.fixture(scope="session")
def invalid_config_type() -> pathlib.Path:
    return (
        pathlib.Path(__file__).parent
        / "../../../../../src/tests/resources/broken-project/unicore-config.md"
    )


@pytest.fixture(scope="session")
def config_with_errors() -> pathlib.Path:
    return (
        pathlib.Path(__file__).parent / "../../../../../src/tests/resources/"
        "test-project/config-with-errors.yaml"
    )


@pytest.fixture(scope="session")
def unicore_config_yaml(mlproject_path) -> pathlib.Path:
    return pathlib.Path(f"{str(mlproject_path)}/unicore-config.yaml")


@pytest.fixture(scope="session")
def unicore_config_json(mlproject_path) -> pathlib.Path:
    return pathlib.Path(f"{str(mlproject_path)}/unicore-config.json")


@pytest.fixture()
def unset_tracking_token_env_var_before_execution():
    if utils.mlflow.TRACKING_TOKEN_ENV_VAR in os.environ:
        del os.environ[utils.mlflow.TRACKING_TOKEN_ENV_VAR]
