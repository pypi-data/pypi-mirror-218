import pathlib

import pytest

import mantik.unicore.config.executable as executable


@pytest.mark.parametrize(
    (
        "environment",
        "expected",
    ),
    [
        (
            executable.Singularity(path=pathlib.Path("image.sif")),
            "srun singularity run "
            "--cleanenv "
            "--env MLFLOW_TRACKING_URI="
            "${MLFLOW_TRACKING_URI:-file://$PWD/mlruns} "
            "${MLFLOW_TRACKING_TOKEN:"
            "+--env MLFLOW_TRACKING_TOKEN=$MLFLOW_TRACKING_TOKEN} "
            "${MLFLOW_EXPERIMENT_NAME:"
            "+--env MLFLOW_EXPERIMENT_NAME=$MLFLOW_EXPERIMENT_NAME} "
            "${MLFLOW_EXPERIMENT_ID:"
            "+--env MLFLOW_EXPERIMENT_ID=$MLFLOW_EXPERIMENT_ID} "
            "image.sif",
        ),
        (
            executable.Python(path=pathlib.Path("/path/to/python/env")),
            "source /path/to/python/env/bin/activate &&",
        ),
    ],
)
def test_create_run_command(environment, expected):
    assert expected == environment.as_execution_command()


@pytest.mark.parametrize(
    (
        "singularity_image",
        "expected",
    ),
    [
        (executable.Singularity(path=pathlib.Path("image.sif")), "image.sif"),
        (
            executable.Singularity(
                path=pathlib.Path("/absolute/path/to/image.sif"), type="local"
            ),
            "image.sif",
        ),
        (
            executable.Singularity(
                path=pathlib.Path("/absolute/path/to/image.sif"), type="remote"
            ),
            "/absolute/path/to/image.sif",
        ),
    ],
)
def test_get_singularity_image_path(
    singularity_image,
    example_config,
    expected,
):
    assert expected == singularity_image._get_singularity_image_path()
