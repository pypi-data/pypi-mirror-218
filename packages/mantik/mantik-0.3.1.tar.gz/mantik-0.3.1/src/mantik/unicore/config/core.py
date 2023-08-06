import dataclasses
import logging
import pathlib
import typing as t

import mantik.unicore.config._base as _base
import mantik.unicore.config._utils as _utils
import mantik.unicore.config.environment as environment
import mantik.unicore.config.read as read
import mantik.unicore.config.resources as _resources
import mantik.utils.env as env


_USERNAME_ENV_VAR = "MANTIK_UNICORE_USERNAME"
_PASSWORD_ENV_VAR = "MANTIK_UNICORE_PASSWORD"
_PROJECT_ENV_VAR = "MANTIK_UNICORE_PROJECT"
_UNICORE_AUTH_SERVER_URL_ENV_VAR = "MANTIK_UNICORE_AUTH_SERVER_URL"

logger = logging.getLogger(__name__)


@dataclasses.dataclass
class Config(_base.ConfigObject):
    """The backend config for the UNICORE MLflow backend."""

    api_url: str
    user: str
    password: str
    project: str
    resources: _resources.Resources
    environment: environment.Environment
    exclude: t.Optional[list] = None

    @classmethod
    def _from_dict(cls, config: t.Dict) -> "Config":
        """

        Parameters
        ----------
        config : t.Dict
            the possible keys to specify inside the config dictionary are:
            REQUIRED:
                - UnicoreApiUrl : str
                    URL to the API of the UNICORE HPC used.

                The other required field MANTIK_USERNAME, MANTIK_PASSWORD
                and MANTIK_PROJECT are inferred from the environment.
            OPTIONAL:
                - Resources : dict
                    Dict of parameters specifying the resources
                    to request on the remote system.
                    More info can be found here:
                    https://sourceforge.net/p/unicore/wiki/Job_Description/
                - Environment : dict
                    Used to build a environment.Environment.
                - Exclude : list
                    List of files or file-patterns
                    that are not sent with the job


        Returns
        -------
        mantik.unicore._config.core.Config

        """
        api_url = _utils.get_required_config_value(
            name="UnicoreApiUrl",
            value_type=str,
            config=config,
        )
        user = env.get_required_env_var(_USERNAME_ENV_VAR)
        password = env.get_required_env_var(_PASSWORD_ENV_VAR)
        project = env.get_required_env_var(_PROJECT_ENV_VAR)
        resources = _resources.Resources.from_dict(
            _utils.get_required_config_value(
                name="Resources",
                value_type=dict,
                config=config,
            )
        )
        config_env = environment.Environment.from_dict(
            _utils.get_required_config_value(
                name="Environment",
                value_type=dict,
                config=config,
            )
        )
        exclude = _utils.get_optional_config_value(
            name="Exclude",
            value_type=list,
            config=config,
        )

        return cls(
            api_url=api_url,
            user=user,
            password=password,
            project=project,
            resources=resources,
            environment=config_env,
            exclude=exclude,
        )

    @classmethod
    def from_filepath(cls, filepath: pathlib.Path) -> "Config":
        """Initialize from a given file."""
        return cls._from_dict(read.read_config(filepath))

    @property
    def files_to_exclude(self) -> t.List[str]:
        if self.exclude is None:
            return []
        return self.exclude

    def _to_dict(self) -> t.Dict:
        key_values = {
            "Project": self.project,
            "Resources": self.resources,
            "Environment": self.environment.variables,
            "User precommand": self.environment.get_precommand(),
            "Executable": self.environment.execution.as_execution_command(),
            "RunUserPrecommandOnLoginNode": False,
        }

        key_values = optional_add_srun_cpus_per_task_to_environment(
            key_values, self.resources.cpus
        )

        return _utils.create_dict_with_not_none_values(**key_values)


def optional_add_srun_cpus_per_task_to_environment(
    key_values: dict, cpus: t.Optional[int]
) -> dict:
    if cpus is None:
        return key_values

    environment = key_values.get("Environment") or {}
    srun_cpus_per_task = environment.get("SRUN_CPUS_PER_TASK")

    if srun_cpus_per_task is None:
        key_values.setdefault("Environment", {})["SRUN_CPUS_PER_TASK"] = cpus
    return key_values
