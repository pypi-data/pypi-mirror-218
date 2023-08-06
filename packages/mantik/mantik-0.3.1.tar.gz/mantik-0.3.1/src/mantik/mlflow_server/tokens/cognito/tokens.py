import dataclasses
import datetime
import email.utils
import typing as t


@dataclasses.dataclass(frozen=True)
class Tokens:
    """Holds AWS Cognito auth tokens."""

    access_token: str
    refresh_token: str
    expires_at: datetime.datetime
    __encoding = "utf-8"

    @classmethod
    def from_json_response(
        cls, response: t.Dict, refresh_token: t.Optional[str] = None
    ) -> "Tokens":
        """Create from JSON response."""
        auth_result = response["AuthenticationResult"]
        access_token = auth_result["AccessToken"]
        if refresh_token is None:
            refresh_token = auth_result["RefreshToken"]
        expires_at = _calculate_expiration_date_from_response(response)
        return cls(
            access_token=access_token,
            refresh_token=refresh_token,
            expires_at=expires_at,
        )


def _calculate_expiration_date_from_response(
    response: t.Dict,
) -> datetime.datetime:
    expires_in_s = response["AuthenticationResult"]["ExpiresIn"]
    created_at_str = response["ResponseMetadata"]["HTTPHeaders"]["date"]
    created_at = email.utils.parsedate_to_datetime(created_at_str)
    expires_at = created_at + datetime.timedelta(seconds=expires_in_s)
    return expires_at
