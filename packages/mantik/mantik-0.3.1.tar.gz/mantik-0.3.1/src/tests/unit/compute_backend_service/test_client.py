import dataclasses
import logging

import mantik.compute_backend_service.client as _client
import mantik.compute_backend_service.models as _models
import mantik.testing.token as testing_token
import mantik.unicore.config.core as core
import mantik.utils as utils

TEST_MLFLOW_TRACKING_URI = "https://test-uri.com"
ENV_VARS = {
    core._USERNAME_ENV_VAR: "test-user",
    core._PASSWORD_ENV_VAR: "test-password",
    core._PROJECT_ENV_VAR: "test-project",
    utils.mlflow.TRACKING_URI_ENV_VAR: TEST_MLFLOW_TRACKING_URI,
}


@dataclasses.dataclass
class FakeSubmittedRun:
    run_id: int = 0
    job_id: int = 0


class TestComputeBackendClient:
    @testing_token.set_token()
    def test_log_level_set(self, tmp_dir_as_test_mantik_folder, caplog):
        with utils.env.env_vars_set(ENV_VARS):
            _ = _client.ComputeBackendClient.from_env()
        _client.set_log_level_from_verbose(verbose=True)
        assert _client.logger.level == logging.DEBUG
        assert "Client initialized" in caplog.text

    @testing_token.set_token()
    def test_submit(
        self,
        requests_mock,
        tmp_dir_as_test_mantik_folder,
        mlproject_path,
        caplog,
    ):
        with utils.env.env_vars_set(ENV_VARS):
            client = _client.ComputeBackendClient.from_env()
            _client.set_log_level_from_verbose(verbose=True)
            experiment_id = 123
            run_id = 0
            unicore_job_id = 1

            expected = _models.SubmitRunResponse(
                experiment_id=experiment_id,
                run_id=run_id,
                unicore_job_id=unicore_job_id,
            )

            # Note: fastapi converts pydantic.BaseModel to dict
            # https://github.com/tiangolo/fastapi/blob/master/fastapi/routing.py#L77
            requests_mock.post(
                f"{client.submit_url}/{experiment_id}",
                json=expected.dict(),
                status_code=201,
            )

            result = client.submit_run(
                experiment_id=experiment_id,
                mlproject_path=mlproject_path,
                mlflow_parameters={"test-parameter": "test-value"},
                backend_config="unicore-config.json",
                entry_point="main",
            )

            assert result.status_code == 201
            assert result.json() == expected.dict()
            assert (
                f"Sending request to compute backend {client.submit_url}"
                in caplog.text
            )
            assert (
                f"Submitting MLproject {mlproject_path} for experiment "
                f"{experiment_id}" in caplog.text
            )
            assert (
                f"Validating MLproject at {mlproject_path} and "
                f"backend config at {mlproject_path}/unicore-config.json"
                in caplog.text
            )
            assert "Validating MLproject configuration." in caplog.text
            assert (
                f"Job submitted successfully with"
                f" experiment_id={experiment_id},"
                f" run_id={run_id},"
                f" unicore_job_id={unicore_job_id}" in caplog.text
            )
