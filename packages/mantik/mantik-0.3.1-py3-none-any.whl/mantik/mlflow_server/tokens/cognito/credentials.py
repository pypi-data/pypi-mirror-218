import abc
import dataclasses
import typing as t


@dataclasses.dataclass(frozen=True)
class Credentials(abc.ABC):
    """Credentials required for authentication.

    Parameters
    ----------
    username : str
        Name of the user.
    secret : str
        The Cognito App Client secret.

    """

    username: str

    @property
    @abc.abstractmethod
    def auth_flow(self) -> str:
        """Return the auth flow type for these credentials."""

    @abc.abstractmethod
    def to_auth_parameters(self) -> t.Dict:
        """Return as auth parameters as required by boto3."""


@dataclasses.dataclass(frozen=True)
class CreateTokenCredentials(Credentials):
    """Credentials required for user-password authentication.

    Parameters
    ----------
    password : str
        Password of the user.

    """

    password: str

    @property
    def auth_flow(self) -> str:
        return "USER_PASSWORD_AUTH"

    def to_auth_parameters(self) -> t.Dict:
        """Return as auth parameters as required by boto3."""
        return {
            "USERNAME": self.username,
            "PASSWORD": self.password,
        }


@dataclasses.dataclass(frozen=True)
class RefreshTokenCredentials(Credentials):
    """Credentials required for refresh token authentication.

    Parameters
    ----------
    refresh_token : str
        The refresh token.

    """

    refresh_token: str

    @property
    def auth_flow(self) -> str:
        return "REFRESH_TOKEN_AUTH"

    def to_auth_parameters(self) -> t.Dict:
        """Return as auth parameters as required by boto3."""
        return {
            "REFRESH_TOKEN": self.refresh_token,
        }
