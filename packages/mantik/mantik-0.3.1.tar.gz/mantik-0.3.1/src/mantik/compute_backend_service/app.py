import fastapi
import mlflow.exceptions
import requests.exceptions as request_exceptions
import starlette.status as status

import mantik.compute_backend_service.api as api
import mantik.compute_backend_service.exceptions as exceptions
import mantik.unicore.exceptions as unicore_exceptions


def create_app(
    docs_url: str, redoc_url: str, openapi_url: str, global_path_prefix: str
) -> fastapi.FastAPI:
    app = fastapi.FastAPI(
        docs_url=global_path_prefix + docs_url,
        redoc_url=global_path_prefix + redoc_url,
        openapi_url=global_path_prefix + openapi_url,
    )
    app.include_router(api.router, prefix=global_path_prefix)
    add_exception_handlers(app)
    return app


def add_exception_handlers(app: fastapi.FastAPI) -> None:
    app.add_exception_handler(
        unicore_exceptions.UnicoreError, exceptions.unicore_exception_handler
    )
    app.add_exception_handler(
        unicore_exceptions.ConfigValidationError,
        exceptions.config_validation_exception_handler,
    )
    app.add_exception_handler(
        request_exceptions.HTTPError,
        exceptions.request_exception_handler,
    )
    app.add_exception_handler(
        ConnectionError,
        exceptions.connection_exception_handler,
    )
    app.add_exception_handler(
        mlflow.exceptions.MlflowException,
        exceptions.mlflow_exception_handler,
    )
    app.add_exception_handler(
        status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
        exceptions.file_too_large_exception_handler,
    )
    app.add_exception_handler(
        status.HTTP_500_INTERNAL_SERVER_ERROR,
        exceptions.internal_exception_handler,
    )
