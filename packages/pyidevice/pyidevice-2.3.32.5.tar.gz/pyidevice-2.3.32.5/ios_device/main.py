import click
from pyidevice.cli.instruments import cli as instruments_cli
from pyidevice.cli.mobile import cli as mobile_cli


def cli():
    cli_commands = click.CommandCollection(sources=[
        instruments_cli,mobile_cli
    ])
    cli_commands()


if __name__ == '__main__':
    cli()
