import click.testing

import mantik.cli.main as main
import mantik.utils as utils


def test_get_logs_with_api_url(fake_client, mantik_env_variables):
    with utils.env.env_vars_set(mantik_env_variables):
        runner = click.testing.CliRunner()
        result = runner.invoke(
            main.cli,
            [
                "runs",
                "info",
                *["--api-url=https://test-uri.com", "test_job_url5"],
            ],
        )

        assert result.exit_code == 0
        assert result.output == (
            "ACL: []\n"
            "BatchSystemID: N/A\n"
            "ConsumedTime:\n"
            "  main: 0:00:05\n"
            "  postCommand: 0:00:06\n"
            "  preCommand: 0:00:04\n"
            "  queued: 0:00:02\n"
            "  stage-in: 0:00:03\n"
            "  stage-out: 0:00:07\n"
            "  total: 0:00:01\n"
            "CurrentTime: '2000-01-06T00:00:00+02:00'\n"
            "ExitCode: '0'\n"
            "Logs: []\n"
            "Name: name\n"
            "Owner: owner\n"
            "Queue: queue\n"
            "ResourceStatus: resourceStatus\n"
            "ResourceStatusMessage: N/A\n"
            "SiteName: siteName\n"
            "Status: SUCCESSFUL\n"
            "StatusMessage: statusMessage\n"
            "SubmissionPreferences: {}\n"
            "SubmissionTime: '2000-01-06T00:00:00+02:00'\n"
            "Tags: []\n"
            "TerminationTime: '2000-01-07T00:00:00+02:00'\n"
            "id: test_job_url5\n"
            "\n"
        )


def test_get_logs_with_config(
    fake_client, example_project_path, mantik_env_variables
):
    with utils.env.env_vars_set(mantik_env_variables):
        runner = click.testing.CliRunner()
        result = runner.invoke(
            main.cli,
            [
                "runs",
                "info",
                *[
                    f"--backend-config={example_project_path}/unicore-config.json",  # noqa
                    "test_job_url7",
                ],
            ],
        )

        assert result.exit_code == 0
        assert result.output == (
            "ACL: []\n"
            "BatchSystemID: N/A\n"
            "ConsumedTime:\n"
            "  main: 0:00:05\n"
            "  postCommand: 0:00:06\n"
            "  preCommand: 0:00:04\n"
            "  queued: 0:00:02\n"
            "  stage-in: 0:00:03\n"
            "  stage-out: 0:00:07\n"
            "  total: 0:00:01\n"
            "CurrentTime: '2000-01-08T00:00:00+02:00'\n"
            "ExitCode: '0'\n"
            "Logs: []\n"
            "Name: name\n"
            "Owner: owner\n"
            "Queue: queue\n"
            "ResourceStatus: resourceStatus\n"
            "ResourceStatusMessage: N/A\n"
            "SiteName: siteName\n"
            "Status: SUCCESSFUL\n"
            "StatusMessage: statusMessage\n"
            "SubmissionPreferences: {}\n"
            "SubmissionTime: '2000-01-08T00:00:00+02:00'\n"
            "Tags: []\n"
            "TerminationTime: '2000-01-09T00:00:00+02:00'\n"
            "id: test_job_url7\n"
            "\n"
        )


def test_get_logs_with_no_option(mantik_env_variables):
    with utils.env.env_vars_set(mantik_env_variables):
        runner = click.testing.CliRunner()
        result = runner.invoke(
            main.cli,
            [
                "runs",
                "info",
                *["test-id1"],
            ],
        )

        assert result.exit_code == 1
        assert isinstance(result.exception, ValueError)
