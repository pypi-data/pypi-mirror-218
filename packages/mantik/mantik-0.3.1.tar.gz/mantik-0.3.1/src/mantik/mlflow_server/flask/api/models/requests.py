import abc

import pydantic

import mantik.mlflow_server.tokens.cognito as _cognito


class TokenRequest(abc.ABC, pydantic.BaseModel):
    """Credentials required for a token request.

    Parameters
    ----------
    username : str
        Name of the user.

    """

    username: str

    @abc.abstractmethod
    def to_cognito_credentials(self) -> _cognito.credentials.Credentials:
        """Return as Cogito credentials."""


class CreateTokenRequest(TokenRequest):
    """Credentials required to create a token.

    Parameters
    ----------
    password : str
        Password of the user.

    """

    password: str

    def to_cognito_credentials(
        self,
    ) -> _cognito.credentials.CreateTokenCredentials:
        return _cognito.credentials.CreateTokenCredentials(
            username=self.username,
            password=self.password,
        )


class RefreshTokenRequest(TokenRequest):
    """Credentials required to refresh a token.

    Parameters
    ----------
    refresh_token : str
        Refresh token.

    """

    refresh_token: str

    def to_cognito_credentials(
        self,
    ) -> _cognito.credentials.RefreshTokenCredentials:
        return _cognito.credentials.RefreshTokenCredentials(
            username=self.username,
            refresh_token=self.refresh_token,
        )
