import click

import auth.cli
import core.cli

from utils.async_utils import async_exec


@click.group()
def cli_app() -> None:
    pass


for command in core.cli.commands:
    cli_app.command()(command)

for command in auth.cli.commands:
    cli_app.command()(command)


async def _test() -> None:
    print('Manage is working fine')


@cli_app.command()
def test() -> None:
    async_exec(_test)


if __name__ == '__main__':
    cli_app()
