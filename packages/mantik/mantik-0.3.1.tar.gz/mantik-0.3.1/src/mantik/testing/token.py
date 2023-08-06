import datetime
import functools
import os
import typing as t

import mantik.authentication.auth as auth
import mantik.authentication.tokens as _tokens
import mantik.utils as utils


def set_token(
    access_token: str = "test-access-token",
    refresh_token: str = "test-refresh-token",
    expires_at: datetime.datetime = datetime.datetime(2020, 1, 1, 2),
) -> t.Callable:
    import freezegun

    def decorate(test_function):
        @functools.wraps(test_function)
        @freezegun.freeze_time("2020-01-01T01:00")
        def wrapper(*args, **kwargs):
            # The client calls `mantik.tracking.init_tracking()`.
            # Thus, we store valid, non-expired tokens before to
            # avoid a refreshing.
            tokens = _tokens.Tokens(
                access_token=access_token,
                refresh_token=refresh_token,
                expires_at=expires_at,
            )
            tokens.write_to_file(auth._MANTIK_TOKEN_FILE)
            test_function(*args, **kwargs)
            os.unsetenv(utils.mlflow.TRACKING_TOKEN_ENV_VAR)

        return wrapper

    return decorate
