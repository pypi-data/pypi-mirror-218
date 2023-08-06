import datetime
import typing as t

import pydantic

import mantik.mlflow_server.tokens.cognito as cognito


class TokenResponse(pydantic.BaseModel):
    """Response for tokens."""

    access_token: str
    expires_at: datetime.datetime

    @classmethod
    def from_cognito_tokens(
        cls, tokens: cognito.tokens.Tokens
    ) -> "TokenResponse":
        """Create from Cognito Tokens."""
        return cls(
            access_token=tokens.access_token,
            expires_at=tokens.expires_at,
        )

    def to_dict(self) -> t.Dict:
        return {
            "AccessToken": self.access_token,
            "ExpiresAt": self.expires_at.isoformat(),
        }


class CreateTokenResponse(TokenResponse):
    """Response for creating tokens."""

    refresh_token: str

    @classmethod
    def from_cognito_tokens(
        cls, tokens: cognito.tokens.Tokens
    ) -> "CreateTokenResponse":
        """Create from Cognito Tokens."""
        return cls(
            access_token=tokens.access_token,
            refresh_token=tokens.refresh_token,
            expires_at=tokens.expires_at,
        )

    def to_dict(self) -> t.Dict:
        return {
            **super().to_dict(),
            "RefreshToken": self.refresh_token,
        }


class RefreshTokenResponse(TokenResponse):
    """Response for refreshing tokens."""
