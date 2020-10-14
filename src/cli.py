"""CLI entrypoints through ``click`` bindings."""

import logging

import click

import src


@click.group()
@click.option(
    "--log_level",
    type=click.Choice(["DEBUG", "INFO", "WARNING"]),
    default="INFO",
    help="Set logging level for both console and file",
)
def cli(log_level):
    """CLI entrypoint."""
    logging.basicConfig(level=log_level)


@cli.command()
def version():
    """Print application version."""
    print(f"src version\t{src.__version__}")
