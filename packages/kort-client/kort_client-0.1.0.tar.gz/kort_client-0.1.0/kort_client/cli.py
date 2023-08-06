import json

import click

from kort_client.api import KortAPI
from kort_client.run import PrintClient

from .config import settings


@click.group()
def cli():
    pass


@cli.command()
@click.argument("config_file", type=click.File("r"))
def setup(config_file):
    config = json.load(config_file)

    if settings.client_id:
        overwrite = click.confirm(
            "Client ID already set. Do you want to overwrite it?", default=False
        )

        if not overwrite:
            return

    print(config)
    if (
        "client_id" not in config
        or "client_secret" not in config
        or "base_url" not in config
    ):
        click.echo("Invalid config file")
        return

    settings.client_id = config["client_id"]
    settings.client_secret = config["client_secret"]
    settings.base_url = config["base_url"]

    settings.save_settings()

    api = KortAPI()

    printer_id = api.get_printer_id()

    api.set_printer_status(printer_id, "offline", "Newly registered printer")

    click.echo("Successfully registered printer")


@cli.command()
def config():
    click.echo("client_id: " + settings.get("client_id", ""))
    click.echo("client_secret: " + settings.get("client_secret", ""))
    click.echo("base_url: " + settings.get("base_url", ""))


@cli.command()
def run():
    click.echo("kort-client is running ...")

    api = KortAPI()
    client = PrintClient(settings, api)

    client.run()


if __name__ == "__main__":
    cli()
