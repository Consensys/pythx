"""This module contains the CLI option and argument decorators."""

import tempfile
from os import path

import click

DEFAULT_STORAGE_PATH = path.join(tempfile.gettempdir(), ".pythx.json")

debug_opt = click.option(
    "--debug",
    "-d",
    default=False,
    is_flag=True,
    envvar="PYTHX_DEBUG",
    help="Provide additional debug output",
)

staging_opt = click.option(
    "--staging",
    default=False,
    is_flag=True,
    envvar="PYTHX_STAGING",
    help="Use the MythX staging environment",
)
config_opt = click.option(
    "--config",
    default=DEFAULT_STORAGE_PATH,
    envvar="PYTHX_CONFIG",
    help="Path to user credentials JSON file",
)
html_opt = click.option(
    "--html", "mode", flag_value="html", help="Get the HTML OpenAPI spec"
)
yaml_opt = click.option(
    "--yaml", "mode", flag_value="yaml", default=True, help="Get the YAML OpenAPI spec"
)
number_opt = click.option(
    "--number",
    default=20,
    type=click.IntRange(min=1, max=100),
    help="The number of most recent analysis jobs to display",
)
bytecode_file_opt = click.option(
    "--bytecode-file",
    "-bf",
    type=click.Path(exists=True),
    default=None,
    help="Path to file containing creation bytecode",
)
source_file_opt = click.option(
    "--source-file",
    "-sf",
    type=click.Path(exists=True),
    default=None,
    help="Path to file containing Solidity source code",
)
interval_opt = click.option(
    "--interval", default=5, type=click.INT, help="Refresh interval"
)
solc_path_opt = click.option(
    "--solc-path",
    type=click.Path(exists=True),
    default=None,
    help="Path to the solc compiler",
)
uuid_arg = click.argument("uuid", type=click.UUID)
no_cache_opt = click.option(
    "--no-cache", is_flag=True, default=False, help="Disable the API's request cache"
)
entrypoint_opt = click.option(
    "--entrypoint",
    "-e",
    type=click.Path(exists=True, readable=True),
    help="The main Solidity file called by the user",
)
