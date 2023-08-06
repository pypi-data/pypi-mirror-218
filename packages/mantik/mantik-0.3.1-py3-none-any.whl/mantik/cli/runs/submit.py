import argparse
import ast
import pathlib
import typing as t

import click

import mantik
import mantik.cli.runs.runs as runs
import mantik.compute_backend_service.client as compute_backend_client
import mantik.utils as utils


def set_logging_callback(ctx, param, value) -> None:  # noqa
    """
    Callback function to set log level from a --verbose flag.

    Note: Unused arguments are part of the click callback signature and
    must be present.
    """
    compute_backend_client.set_log_level_from_verbose(verbose=value)


@runs.cli.command("submit")
@click.argument(
    "mlproject-path",
    type=click.Path(exists=True, file_okay=False, path_type=pathlib.Path),
    required=True,
)
@click.option(
    "--experiment-id",
    default=None,
    type=int,
    help=f"""Experiment ID on MLflow.

        If not specified, it is inferred from the environment variable
        {utils.mlflow.EXPERIMENT_ID_ENV_VAR}.

    """,
)
@click.option(
    "--entry-point",
    required=False,
    default="main",
    show_default=True,
    help="Entrypoint of the MLproject file.",
)
@click.option(
    "--backend-config",
    type=click.Path(dir_okay=False, path_type=pathlib.Path),
    required=True,
    help="Relative path to backend config file.",
)
@click.option(
    "--parameter", "-P", show_default=True, default=lambda: [], multiple=True
)
@click.option(
    "--verbose",
    "-v",
    is_flag=True,
    callback=set_logging_callback,
    help="Set logging to verbose mode.",
)
def run_project(
    mlproject_path: pathlib.Path,
    experiment_id: int,
    entry_point: str,
    backend_config: pathlib.Path,
    parameter: t.List[str],
    verbose: bool,  # noqa
) -> None:
    """Submit an MLflow project as a run to the Mantik Compute Backend.

    `MLPROJECT_PATH` is the path to the MLflow project folder.

    """
    if experiment_id is None:
        experiment_id = utils.env.get_required_env_var(
            utils.mlflow.EXPERIMENT_ID_ENV_VAR
        )
    client = mantik.ComputeBackendClient.from_env()
    parameters = _dict_from_list(parameter)
    response = client.submit_run(
        experiment_id=experiment_id,
        mlflow_parameters=parameters,
        backend_config=backend_config,
        mlproject_path=mlproject_path,
        entry_point=entry_point,
    )

    click.echo(response.content)


def _dict_from_list(parameters: t.List[str]) -> t.Dict:
    return dict([_parse_parameter_from_string(p) for p in parameters])


def _parse_parameter_from_string(parameter: str) -> t.Tuple[str, t.Any]:
    key, value = parameter.split("=", 1)
    return key, _parse_value(value)


def _parse_value(value: t.Any) -> t.Any:
    try:
        return ast.literal_eval(value)
    except (ValueError, SyntaxError):
        # If value is a string, `astr.literal_eval` raises ValueError
        # and in some cases a SyntaxError.
        try:
            return ast.literal_eval(f"'{value}'")
        except (ValueError, SyntaxError):
            raise argparse.ArgumentTypeError(f"Unable to parse {value}")
