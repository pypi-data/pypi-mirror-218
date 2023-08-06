import click.testing

import mantik.cli.main as main
import mantik.utils as utils


def test_get_jobs(fake_client, mantik_env_variables):
    with utils.env.env_vars_set(mantik_env_variables):
        runner = click.testing.CliRunner()
        result = runner.invoke(
            main.cli,
            [
                "runs",
                "list",
                *["--api-url=https://test-uri.com", "-t", "2"],
            ],
        )

        assert result.exit_code == 0
        assert result.output == (
            "Job ID         Submitted At              Queue  Status      \n"
            "------------------------------------------------------------\n"
            "test_job_url9  2000-01-10T00:00:00+0200  queue  SUCCESSFUL  \n"
            "test_job_url8  2000-01-09T00:00:00+0200  queue  SUCCESSFUL  \n"
        )
