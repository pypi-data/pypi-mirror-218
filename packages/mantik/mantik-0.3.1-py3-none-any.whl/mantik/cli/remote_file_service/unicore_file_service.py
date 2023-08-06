import click

import mantik.cli.main as main
import mantik.remote_file_service.unicore_file_service

GROUP_NAME = "unicore-file-service"


@main.cli.group(GROUP_NAME)
def cli() -> None:
    """Interaction with the unicore file service."""


@cli.command("copy-file")
@click.argument("source", type=str, nargs=1, required=True)
@click.argument("target", type=str, nargs=1, required=True)
def copy_file(source: str, target: str) -> None:
    uc_fs = (
        mantik.remote_file_service.unicore_file_service.UnicoreFileService.from_env()  # noqa
    )
    file = uc_fs.copy_file(source=source, target=target)
    click.echo(file)


@cli.command("remove-file")
@click.argument("target", type=str, nargs=1, required=True)
def remove_file(target: str) -> None:
    uc_fs = (
        mantik.remote_file_service.unicore_file_service.UnicoreFileService.from_env()  # noqa
    )
    uc_fs.remove_file(target=target)
    click.echo("File removed!")


@cli.command("create-file")
@click.argument("target", type=str, nargs=1, required=True)
def create_file_if_not_exists_file(target: str) -> None:
    uc_fs = (
        mantik.remote_file_service.unicore_file_service.UnicoreFileService.from_env()  # noqa
    )
    file = uc_fs.create_file_if_not_exists(target=target)
    click.echo(file)


@cli.command("list-directory")
@click.argument("target", type=str, nargs=1, required=True)
def list_directory(target: str) -> None:
    uc_fs = (
        mantik.remote_file_service.unicore_file_service.UnicoreFileService.from_env()  # noqa
    )
    directory = uc_fs.list_directory(target=target)
    click.echo(directory)


@cli.command("create-directory")
@click.argument("target", type=str, nargs=1, required=True)
def create_directory(target: str) -> None:
    uc_fs = (
        mantik.remote_file_service.unicore_file_service.UnicoreFileService.from_env()  # noqa
    )
    directory = uc_fs.create_directory(target=target)
    click.echo(directory)


@cli.command("remove-directory")
@click.argument("target", type=str, nargs=1, required=True)
def remove_directory(target: str) -> None:
    uc_fs = (
        mantik.remote_file_service.unicore_file_service.UnicoreFileService.from_env()  # noqa
    )
    uc_fs.remove_directory(target=target)
    click.echo("Directory removed!")


@cli.command("copy-directory")
@click.argument("source", type=str, nargs=1, required=True)
@click.argument("target", type=str, nargs=1, required=True)
def copy_directory(source: str, target: str) -> None:
    uc_fs = (
        mantik.remote_file_service.unicore_file_service.UnicoreFileService.from_env()  # noqa
    )
    directory = uc_fs.copy_directory(source=source, target=target)
    click.echo(directory)


@cli.command("exists")
@click.argument("path", type=str, nargs=1, required=True)
def exists(path: str) -> None:
    uc_fs = (
        mantik.remote_file_service.unicore_file_service.UnicoreFileService.from_env()  # noqa
    )
    _exists = uc_fs.exists(path=path)
    click.echo(_exists)


@cli.command("user")
def user() -> None:
    uc_fs = (
        mantik.remote_file_service.unicore_file_service.UnicoreFileService.from_env()  # noqa
    )
    click.echo(uc_fs.user)
