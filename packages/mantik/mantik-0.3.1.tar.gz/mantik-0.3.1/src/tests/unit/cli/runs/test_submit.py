import argparse

import click.testing
import pytest

import mantik.cli.main as main
import mantik.cli.runs.submit as submit
import mantik.compute_backend_service.api as api
import mantik.compute_backend_service.client as _client
import mantik.testing.token as testing_token
import mantik.unicore.config.core as core
import mantik.utils as utils
import mantik.utils.mantik_api.credentials as _credentials

TEST_MLFLOW_TRACKING_URI = "https://test-uri.com"
ENV_VARS = {
    core._USERNAME_ENV_VAR: "test-user",
    core._PASSWORD_ENV_VAR: "test-password",
    core._PROJECT_ENV_VAR: "test-project",
    utils.mlflow.TRACKING_URI_ENV_VAR: TEST_MLFLOW_TRACKING_URI,
    utils.mlflow.EXPERIMENT_ID_ENV_VAR: "0",
    _credentials._MANTIK_USERNAME_ENV_VAR: "mantik-user",
    _credentials._MANTIK_PASSWORD_ENV_VAR: "matik_password",
}


@pytest.mark.parametrize(
    ("cli_args", "expected"),
    [
        (
            [
                "--backend-config=unicore-config.json",
            ],
            0,
        ),
        (
            [
                "--backend-config=unicore-config.json",
                "-P a=99",
                "-P b=hello",
            ],
            0,
        ),
        ([], 2),
    ],
)
@testing_token.set_token()
def test_run_project(
    cli_args, expected, requests_mock, mlflow_tracking_uri, example_project_path
):
    cli_args.append(example_project_path)
    with utils.env.env_vars_set(ENV_VARS):
        requests_mock.post(
            f"{TEST_MLFLOW_TRACKING_URI}"
            f"{_client._DEFAULT_COMPUTE_BACKEND_API_PATH}"
            f"{api.SUBMIT_PATH}/{ENV_VARS['MLFLOW_EXPERIMENT_ID']}",
            json=201,
        )

        runner = click.testing.CliRunner()
        result = runner.invoke(main.cli, ["runs", "submit", *cli_args])

        assert result.exit_code == expected


@testing_token.set_token()
def test_run_project_with_absolute_path_for_backend_config(
    requests_mock, mlflow_tracking_uri, example_project_path
):
    cli_args = [
        example_project_path,
        f"--backend-config={example_project_path}/unicore-config.json",
    ]
    with utils.env.env_vars_set(ENV_VARS):
        requests_mock.post(
            f"{TEST_MLFLOW_TRACKING_URI}"
            f"{_client._DEFAULT_COMPUTE_BACKEND_API_PATH}"
            f"{api.SUBMIT_PATH}/{ENV_VARS['MLFLOW_EXPERIMENT_ID']}",
            json=201,
        )

        runner = click.testing.CliRunner()
        result = runner.invoke(main.cli, ["runs", "submit", *cli_args])

        assert result.exit_code == 0


@testing_token.set_token()
def test_run_project_with_set_log_level(
    requests_mock, example_project_path, caplog
):
    with utils.env.env_vars_set(ENV_VARS):
        requests_mock.post(
            f"{TEST_MLFLOW_TRACKING_URI}"
            f"{_client._DEFAULT_COMPUTE_BACKEND_API_PATH}"
            f"{api.SUBMIT_PATH}/{ENV_VARS['MLFLOW_EXPERIMENT_ID']}",
            json=201,
        )
        runner = click.testing.CliRunner()
        _ = runner.invoke(
            main.cli,
            [
                "runs",
                "submit",
                example_project_path,
                f"--backend-config={example_project_path}/unicore-config.json",
                "--verbose",
            ],
        )
        assert "DEBUG" in caplog.text


@pytest.mark.parametrize(
    ("string_list", "expected_dict"),
    [
        (
            [
                "n_components=3",
                "n_components2=2.7",
                "data='/opt/data/temperature_level_128'",
                "url==========",
            ],
            {
                "n_components": 3,
                "n_components2": 2.7,
                "data": "/opt/data/temperature_level_128",
                "url": "=========",
            },
        ),
    ],
)
def test_dict_from_list(string_list, expected_dict):
    assert expected_dict == submit._dict_from_list(string_list)


@pytest.mark.parametrize(
    ("parameter_sting", "expected"),
    [
        ("n_components=3", ("n_components", 3)),
        ("n_components=2.7", ("n_components", 2.7)),
        (
            "data='/opt/data/temperature_level_128_daily_averages_2020.nc'",
            ("data", "/opt/data/temperature_level_128_daily_averages_2020.nc"),
        ),
        (
            'data="/opt/data/temperature_level_128_daily_averages_2020.nc"',
            ("data", "/opt/data/temperature_level_128_daily_averages_2020.nc"),
        ),
        (
            "data=/opt/data/temperature_level_128_daily_averages_2020.nc",
            ("data", "/opt/data/temperature_level_128_daily_averages_2020.nc"),
        ),
        ("url==========", ("url", "=========")),
    ],
)
def test_parse_parameter_from_string(parameter_sting, expected):
    assert expected == submit._parse_parameter_from_string(parameter_sting)


@pytest.mark.parametrize(
    ("string", "expected"),
    [
        ("3", 3),
        ("2.7", 2.7),
        (
            "/opt/data/temperature_level_128_daily_averages_2020.nc",
            "/opt/data/temperature_level_128_daily_averages_2020.nc",
        ),
    ],
)
def test_parse_value(string, expected):
    assert expected == submit._parse_value(string)


def test_parse_value_try_injection():
    injection = "_parse_parameter_from_string('a=2')"
    with pytest.raises(argparse.ArgumentTypeError) as parse_error:
        submit._parse_value(injection)
    assert f"Unable to parse {injection}" in str(parse_error.value)
