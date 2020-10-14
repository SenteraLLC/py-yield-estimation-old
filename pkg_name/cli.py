"""CLI entrypoints through ``click`` bindings."""

import logging

import click

import <pkg_name>


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
    print(f"<pkg_name> version\t{<pkg_name>.__version__}")
