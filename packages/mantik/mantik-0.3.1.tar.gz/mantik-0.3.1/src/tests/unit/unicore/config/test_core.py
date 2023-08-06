import os
import pathlib

import pytest

import mantik.testing as testing
import mantik.unicore.config as _config
import mantik.unicore.config.executable as executable
import mantik.unicore.exceptions as exceptions


class TestConfig:
    @pytest.mark.parametrize(
        ("env_vars", "d", "expected"),
        [
            # ([], {}, ValueError()),
            # Test cases: environment variables not set.
            (
                testing.config.ALL_ENV_VARS[0],
                {},
                exceptions.ConfigValidationError(),
            ),
            (
                testing.config.ALL_ENV_VARS[:2],
                {},
                exceptions.ConfigValidationError(),
            ),
            (
                testing.config.ALL_ENV_VARS,
                {},
                exceptions.ConfigValidationError(),
            ),
            # Test case: backend config missing Resources section.
            (
                testing.config.ALL_ENV_VARS,
                {"Queue": "batch"},
                exceptions.ConfigValidationError(),
            ),
            # Test case: Everything correct.
            (
                testing.config.ALL_ENV_VARS,
                {
                    "UnicoreApiUrl": "test-url",
                    "Environment": {
                        "Singularity": {
                            "Path": "image.sif",
                        },
                    },
                    "Resources": {"Queue": "batch"},
                },
                testing.config._create_config(
                    resources=_config.resources.Resources(queue="batch"),
                ),
            ),
            # Test case: Local Singularity image given.
            (
                testing.config.ALL_ENV_VARS,
                {
                    "UnicoreApiUrl": "test-url",
                    "Resources": {"Queue": "batch"},
                    "Environment": {
                        "Singularity": {
                            "Path": "image.sif",
                        },
                    },
                },
                testing.config._create_config(
                    resources=_config.resources.Resources(queue="batch"),
                ),
            ),
            # Test case: Remote Singularity image given.
            (
                testing.config.ALL_ENV_VARS,
                {
                    "UnicoreApiUrl": "test-url",
                    "Resources": {"Queue": "batch"},
                    "Environment": {
                        "Singularity": {
                            "Path": "/absolute/path/to/image.sif",
                            "Type": "remote",
                        },
                    },
                },
                testing.config._create_config(
                    resources=_config.resources.Resources(queue="batch"),
                    env=_config.environment.Environment(
                        execution=executable.Singularity(
                            path=pathlib.Path("/absolute/path/to/image.sif"),
                            type="remote",
                        ),
                    ),
                ),
            ),
            # Test case: More variables and modules given.
            (
                testing.config.ALL_ENV_VARS,
                {
                    "UnicoreApiUrl": "test-url",
                    "Resources": {"Queue": "batch"},
                    "Environment": {
                        "Singularity": {
                            "Path": "/absolute/path/to/image.sif",
                            "Type": "remote",
                        },
                        "Variables": {"TEST_ENV_VAR": "value"},
                        "Modules": [
                            "TensorFlow/2.5.0-Python-3.8.5",
                            "Horovod/0.23.0-Python-3.8.5",
                            "PyTorch/1.8.1-Python-3.8.5",
                        ],
                    },
                },
                testing.config._create_config(
                    resources=_config.resources.Resources(queue="batch"),
                    env=_config.environment.Environment(
                        execution=executable.Singularity(
                            path=pathlib.Path("/absolute/path/to/image.sif"),
                            type="remote",
                        ),
                        modules=[
                            "TensorFlow/2.5.0-Python-3.8.5",
                            "Horovod/0.23.0-Python-3.8.5",
                            "PyTorch/1.8.1-Python-3.8.5",
                        ],
                        variables={"TEST_ENV_VAR": "value"},
                    ),
                ),
            ),
            # Test case: Remote Singularity image given but relative path.
            (
                testing.config.ALL_ENV_VARS,
                {
                    "UnicoreApiUrl": "test-url",
                    "Resources": {"Queue": "batch"},
                    "Environment": {
                        "Singularity": {
                            "Path": "../relative/path/to/image.sif",
                            "Type": "remote",
                        },
                    },
                },
                exceptions.ConfigValidationError(),
            ),
            # Test case: Config entry has incorrect type.
            (
                testing.config.ALL_ENV_VARS,
                {
                    "UnicoreApiUrl": "test-url",
                    "Resources": {"Queue": "batch", "Nodes": "incorrect type"},
                },
                exceptions.ConfigValidationError(),
            ),
        ],
    )
    @pytest.mark.usefixtures("unset_tracking_token_env_var_before_execution")
    def test_from_dict(self, env_vars, d, expected):
        for key in env_vars:
            os.environ[key] = testing.config.DEFAULT_ENV_VAR_VALUE

        with testing.contexts.expect_raise_if_exception(expected):
            result = _config.core.Config.from_dict(d)

            assert result == expected

    @pytest.mark.parametrize(
        ("config", "expected"),
        [
            # Test case: Only project, resources and
            # environment are included in the returned dict.
            (
                _config.core.Config(
                    api_url="not_included",
                    user="not_included",
                    password="not_included",
                    project="test-project",
                    resources=_config.resources.Resources(
                        queue="batch",
                    ),
                    environment=_config.environment.Environment(
                        execution=executable.Singularity(
                            path=pathlib.Path("test-image")
                        ),
                    ),
                ),
                {
                    "Project": "test-project",
                    "Resources": {"Queue": "batch"},
                    "Executable": "srun singularity run --cleanenv --env "
                    "MLFLOW_TRACKING_URI=${MLFLOW_TRACKING_URI:"
                    "-file://$PWD/mlruns} "
                    "${MLFLOW_TRACKING_TOKEN:+--env "
                    "MLFLOW_TRACKING_TOKEN=$MLFLOW_TRACKING_TOKEN} "
                    "${MLFLOW_EXPERIMENT_NAME:+--env "
                    "MLFLOW_EXPERIMENT_NAME=$MLFLOW_EXPERIMENT_NAME} "
                    "${MLFLOW_EXPERIMENT_ID:+--env "
                    "MLFLOW_EXPERIMENT_ID=$MLFLOW_EXPERIMENT_ID} test-image",
                    "RunUserPrecommandOnLoginNode": "false",
                },
            ),
            # Test case: All given values included.
            (
                _config.core.Config(
                    api_url="not_included",
                    user="not_included",
                    password="not_included",
                    project="test-project",
                    resources=_config.resources.Resources(
                        queue="batch",
                        runtime="1h",
                        nodes=2,
                        cpus=48,
                        cpus_per_node=24,
                        memory="10GiB",
                        reservation="test-reservation",
                        node_constraints="test-node-constraints",
                        qos="test-qos",
                    ),
                    environment=_config.environment.Environment(
                        execution=executable.Singularity(
                            path=pathlib.Path("test-image"),
                        ),
                        variables={"TEST": "test"},
                    ),
                ),
                {
                    "Project": "test-project",
                    "Resources": {
                        "Queue": "batch",
                        "Runtime": "1h",
                        "Nodes": 2,
                        "CPUs": 48,
                        "CPUsPerNode": 24,
                        "Memory": "10GiB",
                        "Reservation": "test-reservation",
                        "NodeConstraints": "test-node-constraints",
                        "QoS": "test-qos",
                    },
                    "Environment": {"TEST": "test", "SRUN_CPUS_PER_TASK": 48},
                    "Executable": "srun singularity run --cleanenv --env "
                    "MLFLOW_TRACKING_URI=${MLFLOW_TRACKING_URI:"
                    "-file://$PWD/mlruns} "
                    "${MLFLOW_TRACKING_TOKEN:+--env "
                    "MLFLOW_TRACKING_TOKEN=$MLFLOW_TRACKING_TOKEN} "
                    "${MLFLOW_EXPERIMENT_NAME:+--env "
                    "MLFLOW_EXPERIMENT_NAME=$MLFLOW_EXPERIMENT_NAME} "
                    "${MLFLOW_EXPERIMENT_ID:+--env "
                    "MLFLOW_EXPERIMENT_ID=$MLFLOW_EXPERIMENT_ID} test-image",
                    "RunUserPrecommandOnLoginNode": "false",
                },
            ),
        ],
    )
    def test_to_dict(self, config, expected):
        result = config.to_dict()

        assert result == expected
