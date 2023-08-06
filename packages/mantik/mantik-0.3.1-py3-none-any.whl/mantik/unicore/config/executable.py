import abc
import dataclasses
import logging
import pathlib
import typing as t

import mantik.unicore.config._utils as _utils
import mantik.unicore.exceptions as exceptions
import mantik.utils.mlflow as mlflow_utils

logger = logging.getLogger(__name__)

_LOCAL_IMAGE_TYPE = "local"
_REMOTE_IMAGE_TYPE = "remote"
_ALLOWED_IMAGE_TYPES = [_LOCAL_IMAGE_TYPE, _REMOTE_IMAGE_TYPE]


@dataclasses.dataclass
class Execution:
    """Execution environment used for executing a python script."""

    path: str

    @property
    @abc.abstractmethod
    def path_has_to_be_checked(self) -> bool:
        raise NotImplementedError

    @abc.abstractmethod
    def as_execution_command(self) -> str:
        raise NotImplementedError

    @classmethod
    @abc.abstractmethod
    def from_dict(cls, config: t.Dict):
        raise NotImplementedError


@dataclasses.dataclass
class Singularity(Execution):
    """Information about a Singularity image.

    Parameters
    ----------
    path : pathlib.Path
        Path to the image.
    type : str, default="local"
        Image type, i.e. if stored locally or remotely.


    """

    path: pathlib.Path
    type: str = _LOCAL_IMAGE_TYPE

    def __post_init__(self) -> None:
        """Check that the given type is correct."""
        self.type = self.type.lower()
        self._ensure_valid_path_type()
        self._ensure_path_conform_to_type()

    @property
    def path_has_to_be_checked(self) -> bool:
        return self.type == _LOCAL_IMAGE_TYPE

    def _ensure_valid_path_type(self) -> None:
        if self.type not in _ALLOWED_IMAGE_TYPES:
            raise exceptions.ConfigValidationError(
                f"The given Apptainer image type {self.type!r} "
                "is not supported, "
                "the supported ones are: "
                f"{exceptions.list_to_string(_ALLOWED_IMAGE_TYPES)}."
            )

    def _ensure_path_conform_to_type(self) -> None:
        if self._remote_image_and_relative_path_given():
            raise exceptions.ConfigValidationError(
                f"If image type {self.type!r} is given for an Apptainer "
                "image, the given path must be absolute. "
                f"The given path is: {self.path.as_posix()!r}."
            )
        elif self._local_image_and_relative_path_given():
            logger.warning(
                (
                    "Path for Singularity image of type %s is assumed to be "
                    "relative to the MLflow project directory"
                ),
                _LOCAL_IMAGE_TYPE,
            )

    def _remote_image_and_relative_path_given(self) -> bool:
        return self.type == _REMOTE_IMAGE_TYPE and not self.path.is_absolute()

    def _local_image_and_relative_path_given(self) -> bool:
        return self.type == _LOCAL_IMAGE_TYPE and not self.path.is_absolute()

    @classmethod
    def from_dict(cls, config: t.Dict) -> "Singularity":
        singularity = _utils.get_required_config_value(
            name="Singularity",
            value_type=dict,
            config=config,
        )
        path = _utils.get_required_config_value(
            name="Path",
            value_type=pathlib.Path,
            config=singularity,
        )
        type_ = _utils.get_optional_config_value(
            name="Type",
            value_type=str,
            config=singularity,
            default=_LOCAL_IMAGE_TYPE,
        )
        return cls(
            path=path,
            type=type_,
        )

    @property
    def is_local(self) -> bool:
        """Return whether the image is stored locally."""
        return self.type == _LOCAL_IMAGE_TYPE

    @property
    def is_remote(self) -> bool:
        """Return whether the image is stored remotely."""
        return self.type == _REMOTE_IMAGE_TYPE

    @property
    def name(self) -> str:
        """Return the file name of the image."""
        return self.path.name

    @property
    def path_str(self) -> str:
        """Return the path as a string"""
        return self.path.as_posix()

    def path_as_absolute_to(self, root: pathlib.Path) -> pathlib.Path:
        """Return the image's path as an absolute with the given root."""
        if self.path.is_absolute():
            return self.path
        path = root / self.path
        logger.warning(
            (
                "Assuming that given Singularity image path %s is relative to "
                "directory %s, hence assuming absolute path %s"
            ),
            self.path,
            root,
            path,
        )
        return path

    def as_execution_command(self) -> str:
        singularity_image_path = self._get_singularity_image_path()
        return (
            "srun singularity run "
            "--cleanenv "
            # Pass MLFLOW_TRACKING_URI variable if set, otherwise set to default
            # folder
            f"{_create_env_var_str(mlflow_utils.TRACKING_URI_ENV_VAR, default='file://$PWD/mlruns')} "  # noqa
            # Pass tracking  token if set
            f"{_create_optional_env_str(mlflow_utils.TRACKING_TOKEN_ENV_VAR)} "
            # Pass MLFLOW_EXPERIMENT_NAME variable if set
            f"{_create_optional_env_str(mlflow_utils.EXPERIMENT_NAME_ENV_VAR)} "
            # Pass Experiment ID if set
            f"{_create_optional_env_str(mlflow_utils.EXPERIMENT_ID_ENV_VAR)} "
            f"{singularity_image_path}"
        )

    def _get_singularity_image_path(
        self,
    ) -> str:
        if self.is_local:
            return self.name
        logger.warning(
            "The image is assumed to be already present "
            "in the remote system at the specified path."
        )
        return self.path_str


def _create_env_var_str(name: str, default: str) -> str:
    return f"--env {name}=${{{name}:-{default}}}"


def _create_optional_env_str(env_var_name: str) -> str:
    """Create a --env string for singularity command if variable is set."""
    return f"${{{env_var_name}:+--env {env_var_name}=${env_var_name}}}"


@dataclasses.dataclass
class Python(Execution):
    """Python virtual environment used for executing a python script."""

    path: pathlib.Path

    def __post_init__(self) -> None:
        """Check that the given type is correct."""
        self._ensure_venv_path_is_absolute()

    @property
    def path_has_to_be_checked(self) -> bool:
        return False

    @classmethod
    def from_dict(cls, config: t.Dict) -> "Python":
        if isinstance(config["Python"], dict):
            python_dict = _utils.get_required_config_value(
                name="Python",
                value_type=dict,
                config=config,
            )
            python_path = _utils.get_required_config_value(
                name="Path",
                value_type=pathlib.Path,
                config=python_dict,
            )
        else:
            python_path = _utils.get_required_config_value(
                name="Python",
                value_type=pathlib.Path,
                config=config,
            )
        return cls(
            path=python_path,
        )

    def _ensure_venv_path_is_absolute(self) -> None:
        if not self.path.is_absolute():
            raise exceptions.ConfigValidationError(
                "The given path to the Python Venv must be absolute. "
                f"The given path is: {self.path.as_posix()!r}."
            )

    def as_execution_command(self) -> str:
        return f"source {self.path}/bin/activate &&"
