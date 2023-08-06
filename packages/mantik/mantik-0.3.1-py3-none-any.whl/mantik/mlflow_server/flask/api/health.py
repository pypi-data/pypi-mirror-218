import flask

import mantik.mlflow_server.flask.api.tokens as _tokens
import mantik.mlflow_server.flask.app as _app
import mantik.mlflow_server.flask.skip as skip

app = _app.app


HEALTH_CHECK_API_PATH = f"{_tokens._API_PATH_PREFIX}/health"


@app.route(HEALTH_CHECK_API_PATH, methods=["GET"])
@skip.skip_authentication
def health_check() -> flask.Response:
    """Return the health check response."""
    return flask.make_response("I'm healthy!", 200)
