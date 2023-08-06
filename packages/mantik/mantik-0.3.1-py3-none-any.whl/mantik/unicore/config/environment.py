import dataclasses
import os
import re
import typing as t

import mantik.unicore.config._base as _base
import mantik.unicore.config._utils as _utils
import mantik.unicore.config.executable as executable
import mantik.unicore.exceptions as exceptions

_MLFLOW_ENV_VAR_PREFIX = "MLFLOW_"
_ALLOWED_EXECUTABLES = {
    "Singularity": executable.Singularity,
    "Python": executable.Python,
}


@dataclasses.dataclass
class Environment(_base.ConfigObject):
    """Part of the backend-config where all variables
    concerning the running environment are stored."""

    execution: executable.Execution
    variables: t.Optional[dict] = None
    modules: t.Optional[list] = None

    @classmethod
    def _from_dict(cls, config: t.Dict) -> "Environment":
        variables = _utils.get_optional_config_value(
            name="Variables",
            value_type=dict,
            config=config,
        )
        modules = _utils.get_optional_config_value(
            name="Modules",
            value_type=list,
            config=config,
        )
        return cls(
            execution=_get_environment(config).from_dict(config),
            modules=modules,
            variables=variables,
        )

    def __post_init__(self):
        """Add all MLflow environment variables to the environment."""
        self.variables = _add_mlflow_env_vars(self.variables)

    def _to_dict(self) -> t.Dict:
        pass

    def get_precommand(self):
        if self.modules is not None:
            return f"module load {' '.join(self.modules)}"
        return None


def _get_environment(config: t.Dict) -> t.Type[executable.Execution]:
    envs = [env for env in _ALLOWED_EXECUTABLES if env in config]
    return _get_only_one_environment(envs)


def _get_only_one_environment(
    env_found: t.List,
) -> t.Type[executable.Execution]:
    if not env_found:
        raise exceptions.ConfigValidationError(
            "No execution environment defined in config, "
            "the allowed environments are: "
            f"{exceptions.list_to_string(_ALLOWED_EXECUTABLES.keys())}."
        )
    elif len(env_found) > 1:
        raise exceptions.ConfigValidationError(
            "Only one execution environment is allowed, "
            "but in config these have been found: "
            f"{exceptions.list_to_string(env_found)}."
        )
    return _ALLOWED_EXECUTABLES[env_found[0]]


def _add_mlflow_env_vars(environment: t.Optional[t.Dict]) -> t.Optional[t.Dict]:
    mlflow_env_vars = _get_mlflow_env_vars()
    if mlflow_env_vars:
        if environment is None:
            return mlflow_env_vars
        return {**mlflow_env_vars, **environment}
    return environment


def _get_mlflow_env_vars() -> t.Dict:
    pattern = re.compile(rf"{_MLFLOW_ENV_VAR_PREFIX}\w+")
    return {
        key: value for key, value in os.environ.items() if pattern.match(key)
    }
