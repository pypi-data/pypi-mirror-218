import pathlib

import mlflow.exceptions
import pytest

import mantik.testing as testing
import mantik.unicore.config.environment as environment
import mantik.unicore.config.validate as project_config
import mantik.unicore.exceptions as exceptions


class TestConfigValidator:
    @pytest.mark.parametrize(
        ("mlproject_path", "config_path", "expected"),
        [
            # Test case: config path is not absolute
            (
                "/absolute/path",
                "relative/path",
                pathlib.Path("/absolute/path/relative/path"),
            ),
            # Test case: both paths are absolute
            (
                "/absolute/path",
                "/absolute/path/config",
                pathlib.Path("/absolute/path/config"),
            ),
        ],
    )
    def test_config_absolute_path(self, mlproject_path, config_path, expected):
        config = project_config.ProjectValidator(
            mlproject_path, config_path, {}, "main"
        )
        assert config.config_absolute_path == expected

    @pytest.mark.parametrize(
        ("mlproject_path", "config_path", "expected"),
        [
            # Test case: config path is not absolute
            ("/absolute/path", "relative/path", pathlib.Path("relative/path")),
            # Test case: both paths are absolute
            ("/absolute/path", "/absolute/path/config", pathlib.Path("config")),
        ],
    )
    def test_config_relative_path(self, mlproject_path, config_path, expected):
        config = project_config.ProjectValidator(
            mlproject_path, config_path, {}, "main"
        )
        assert config.config_relative_path == expected

    @pytest.mark.parametrize(
        ("fake_mlproject_path", "config_path", "error_message"),
        [
            # Test case: MLproject path is not absolute
            (
                "absolute/path",
                "relative/path",
                "ML project path must be an absolute path, "
                "but 'absolute/path' was given.",
            ),
            # Test case: MLproject path does not exist
            (
                "/absolute/path",
                "relative/path",
                "ML project path not found at '/absolute/path', "
                "check that the given path is correct.",
            ),
            # Test case: config path does not exist
            (
                "ml_project_resource",
                "false/path/to/config.yml",
                "Config not found at "
                "'ml_project_resource/false/path/to/config.yml', "
                "check that the given path is correct.",
            ),
            # Test case: config path is from another project
            (
                "ml_project_resource",
                "invalid_config_type",
                "Config file is not in the ML project directory, "
                "check that the given paths "
                "are correct:\nConfig file: "
                "'invalid_config_type'\nML project directory: "
                "'ml_project_resource'",
            ),
            # Test case: config is incorrect
            (
                "ml_project_resource",
                "config_with_errors",
                "Config is missing entry for key 'Environment'",
            ),
        ],
    )
    def test_validate(
        self,
        fake_mlproject_path,
        config_path,
        error_message,
        mlproject_path,
        invalid_config_type,
        config_with_errors,
    ):
        with pytest.raises(exceptions.ConfigValidationError) as e:
            final_mlproject_path = fake_mlproject_path
            if fake_mlproject_path == "ml_project_resource":
                final_mlproject_path = mlproject_path

            if config_path == "invalid_config_type":
                config_path = invalid_config_type
            if config_path == "config_with_errors":
                config_path = config_with_errors

            mlproject_config = project_config.ProjectValidator(
                final_mlproject_path, config_path, {}, "main"
            )
            mlproject_config.validate()

        assert str(e.value) == error_message.replace(
            "ml_project_resource", mlproject_path.as_posix()
        ).replace(
            "invalid_config_type", invalid_config_type.as_posix()
        ).replace(
            "config_with_errors", config_with_errors.as_posix()
        )

    @pytest.mark.parametrize(
        ("execution_dict", "expected", "error_message"),
        [
            # Test case: local singularity path does not exist
            (
                {
                    "Singularity": {
                        "Path": "non-existent-image",
                        "Type": "local",
                    }
                },
                exceptions.ConfigValidationError(),
                "The path '"
                "mlproject_path/non-existent-image' "
                "given as execution environment was not found, "
                "check that the given path is correct. "
                "The path must be relative to the ML project path.",
            ),
            # Test case: image exists
            (
                {"Singularity": {"Path": "mantik-test.sif", "Type": "local"}},
                None,
                None,
            ),
            # Test case: image is remote and path absolute
            (
                {
                    "Singularity": {
                        "Path": "/absolute/remote/image",
                        "Type": "remote",
                    }
                },
                None,
                None,
            ),
            # Test case: image is remote and path relative
            (
                {
                    "Singularity": {
                        "Path": "relative/remote/image",
                        "Type": "remote",
                    }
                },
                exceptions.ConfigValidationError(),
                "If image type 'remote' is given for an Apptainer image, "
                "the given path must be absolute. "
                "The given path is: 'relative/remote/image'.",
            ),
            # Test case: python venv has relative path
            (
                {
                    "Python": {
                        "Path": "relative/remote/image",
                    }
                },
                exceptions.ConfigValidationError(),
                "The given path to the Python Venv must be absolute. "
                "The given path is: 'relative/remote/image'.",
            ),
        ],
    )
    def test_validate_execution_path(
        self, mlproject_path, execution_dict, expected, error_message
    ):
        with testing.contexts.expect_raise_if_exception(expected) as e:
            config = project_config.ProjectValidator(
                mlproject_path, "config_path", {}, "main"
            )
            execution = environment._get_environment(
                config=execution_dict
            ).from_dict(execution_dict)
            assert config._validate_execution_path(execution) is expected
        if error_message is not None:
            assert str(e.value) == error_message.replace(
                "mlproject_path", mlproject_path.as_posix()
            )

    @pytest.mark.parametrize(
        ("entry_point", "parameters", "expected"),
        [
            (
                "this-entry-point-does-not-exist",
                {},
                mlflow.exceptions.ExecutionException(
                    "Could not find this-entry-point-does-not-exist "
                    "among entry points ['main'] "
                    "or interpret this-entry-point-does-not-exist "
                    "as a runnable script. "
                    "Supported script file extensions: ['.py', '.sh']"
                ),
            ),
            ("main", {}, None),
        ],
    )
    def test_validate_ml_project_file(
        self, mlproject_path, entry_point, parameters, expected
    ):
        with testing.contexts.expect_raise_if_exception(expected) as e:
            config = project_config.ProjectValidator(
                mlproject_path, "unicore-config.yaml", parameters, entry_point
            )
            config.validate()
            if expected is not None:
                assert str(e.value) == expected.message
