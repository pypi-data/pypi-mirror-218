import os
import pathlib

import pytest

import mantik.testing as testing
import mantik.unicore.config.environment as environment
import mantik.unicore.config.executable as executable
import mantik.unicore.exceptions as exceptions


class TestEnvironment:
    @pytest.mark.parametrize(
        ("env_vars", "d", "expected"),
        [
            (
                testing.config.ALL_ENV_VARS,
                {
                    "Singularity": {
                        "Path": "image.sif",
                    },
                },
                testing.config._create_singularity_environment(
                    path=pathlib.Path("image.sif")
                ),
            ),
            (
                testing.config.ALL_ENV_VARS,
                {"Python": "/path/to/venv"},
                testing.config._create_python_environment(
                    path=pathlib.Path("/path/to/venv")
                ),
            ),
            (
                testing.config.ALL_ENV_VARS,
                {"Python": {"Path": "/path/to/venv"}},
                testing.config._create_python_environment(
                    path=pathlib.Path("/path/to/venv")
                ),
            ),
        ],
    )
    def test_from_dict(self, monkeypatch, env_vars, d, expected):
        if "MLFLOW_TRACKING_TOKEN" in os.environ:
            del os.environ["MLFLOW_TRACKING_TOKEN"]
        if "MLFLOW_EXPERIMENT_ID" in os.environ:
            del os.environ["MLFLOW_EXPERIMENT_ID"]
        for key in env_vars:
            os.environ[key] = testing.config.DEFAULT_ENV_VAR_VALUE

        with testing.contexts.expect_raise_if_exception(expected):
            result = environment.Environment.from_dict(d)

            assert result == expected


@pytest.mark.parametrize(
    ("config", "expected", "error_message"),
    [
        ({"Singularity": {}}, executable.Singularity, None),
        (
            {"Singularity": {}, "Python": {}},
            exceptions.ConfigValidationError(),
            "Only one execution environment is allowed, "
            "but in config these have been "
            "found: 'Singularity', 'Python'.",
        ),
        (
            {"Resources": {}},
            exceptions.ConfigValidationError(),
            "No execution environment defined in config, "
            "the allowed environments are: "
            "'Singularity', 'Python'.",
        ),
    ],
)
def test_get_environment(config, expected, error_message):
    with testing.contexts.expect_raise_if_exception(expected) as e:
        assert environment._get_environment(config) == expected
    if error_message is not None:
        assert str(e.value) == error_message


@pytest.mark.parametrize(
    (
        "modules",
        "expected",
    ),
    [
        (
            None,
            None,
        ),
        (
            ["Module1", "Module2"],
            "module load Module1 Module2",
        ),
    ],
)
def test_create_precommand(modules, expected):
    env = testing.config._create_python_environment(
        modules=modules, path=pathlib.Path("/path/to/venv")
    )
    assert expected == env.get_precommand()
