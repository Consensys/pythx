"""Console script for PythX.

This script aims to be an example of how PythX can be used as a developer-friendly
library around the MythX smart contract security analysis API.
"""
import json
import logging
import os
import sys
import tempfile
import time
from collections import defaultdict
from copy import copy
from distutils import spawn
from os import environ, path
from subprocess import check_output

import click
from tabulate import tabulate

from pythx.api import Client

if environ.get("PYTHX_DEBUG") is not None:
    logging.basicConfig(level=logging.DEBUG)
else:
    logging.basicConfig(level=logging.ERROR)

LOGGER = logging.getLogger("pythx-cli")
DEFAULT_STORAGE_PATH = path.join(tempfile.gettempdir(), ".pythx.json")
CONFIG_KEYS = ("access", "refresh", "username", "password")

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


def parse_config(config_path, tokens_required=False):
    """Recover the user configuration file.

    This file holds their most recent access and refresh JWT tokens. It allows PythX to
    restore the user's login state across executions.

    :param config_path: The configuration file's path
    :param tokens_required: Raise an error if the tokens are required but missing
    :return:
    """
    with open(config_path, "r") as config_f:
        config = json.load(config_f)
    keys_present = all(k in config for k in CONFIG_KEYS)
    if not (type(config) == dict and keys_present):
        click.echo(
            "Malformed config file at {} doesn't contain required keys {}".format(
                config_path, CONFIG_KEYS
            )
        )
        sys.exit(1)
    if tokens_required and not (config["access"] and config["refresh"]):
        click.echo(
            "Malformed config file at {} does not contain access and refresh token".format(
                config_path
            )
        )
        sys.exit(1)
    return config


def update_config(config_path, client):
    """Update the user configuration file with the latest login data.

    The stored data encompasses the API password, the user's Ethereum address, and the
    latest access and refresh tokens.

    :param config_path: The configuration file's path
    :param client: The client instance to get the latest information from
    """
    with open(config_path, "w+") as config_f:
        json.dump(
            {
                "username": client.eth_address,
                "password": client.password,
                "access": client.access_token,
                "refresh": client.refresh_token,
            },
            config_f,
        )


def recover_client(config_path, staging=False, exit_on_missing=False):
    """A simple helper method to recover a client instance based on a user config.

    :param config_path: The configuration file's path
    :param staging: A boolean to denote whether to use staging or not
    :param exit_on_missing: Return if the file is missing
    :return:
    """
    if not path.isfile(config_path):
        if exit_on_missing:
            return None
        # config doesn't exist - assume first use
        eth_address = environ.get("PYTHX_USERNAME") or click.prompt(
            "Please enter your Ethereum address",
            type=click.STRING,
            default="0x0000000000000000000000000000000000000000",
        )
        password = environ.get("PYTHX_PASSWORD") or click.prompt(
            "Please enter your MythX password",
            type=click.STRING,
            hide_input=True,
            default="trial",
        )
        c = Client(eth_address=eth_address, password=password, staging=staging)
        c.login()
        update_config(config_path=config_path, client=c)
    else:
        config = parse_config(config_path, tokens_required=True)
        c = Client(
            eth_address=config["username"],
            password=config["password"],
            access_token=config["access"],
            refresh_token=config["refresh"],
            staging=staging,
        )
    return c


def ps_core(config, staging, number):
    """A helper method to retrieve data from the analysis list endpoint.

    This functionality is used in the :code:`pythx ps`, as well as the :code:`pythx top`
    subcommands.

    :param config: The configuration file's path
    :param staging: Boolean to denote whether to use the MythX staging deployment
    :param number: The number of analyses to retrieve
    :return: The API response as AnalysisList domain model
    """
    c = recover_client(config_path=config, staging=staging)
    if c.eth_address == "0x0000000000000000000000000000000000000000":
        click.echo(
            (
                "This functionality is only available to registered users. "
                "Head over to https://mythx.io/ and register a free account to "
                "list your past analyses. Alternatively, you can look up the "
                "status of a specific job by calling 'pythx status <uuid>'."
            )
        )
        sys.exit(0)
    resp = c.analysis_list()
    # TODO: paginate if too few analyses
    resp.analyses = resp.analyses[: number + 1]
    update_config(config_path=config, client=c)
    return resp


def get_source_location_by_offset(filename, offset):
    """Retrieve the Solidity source file's location based on the source map offset.

    :param filename: The Solidity file to analyze
    :param offset: The source map's offset
    :return: The line and column number
    """
    overall = 0
    line_ctr = 0
    with open(filename) as f:
        for line in f:
            line_ctr += 1
            overall += len(line)
            if overall >= offset:
                return line_ctr, overall - offset
    LOGGER.error(
        "Error finding the source location in {} for offset {}".format(filename, offset)
    )
    sys.exit(1)


def compile_from_source(source_path: str, solc_path: str = None):
    """A simple wrapper around solc to compile Solidity source code.

    :param source_path: The source file's path
    :param solc_path: The path to the solc compiler
    :return: The parsed solc compiler JSON output
    """
    solc_path = spawn.find_executable("solc") if solc_path is None else solc_path
    if solc_path is None:
        # user solc path invalid or no default "solc" command found
        click.echo("Invalid solc path. Please make sure solc is on your PATH.")
        sys.exit(1)
    solc_command = [
        solc_path,
        "--combined-json",
        "ast,bin,bin-runtime,srcmap,srcmap-runtime",
        source_path,
    ]
    output = check_output(solc_command)
    return json.loads(output)


@click.group()
def cli():
    """The basic click CLI command group to register our subcommands under."""
    pass  # pragma: no cover


@cli.command(help="Login to your MythX account")
@staging_opt
@config_opt
def login(staging, config):
    """Perform a login action on the API

    :param staging: Boolean whether to use the MythX staging deployment
    :param config: The configuration file's path
    """
    c = recover_client(config, staging)
    login_resp = c.login()
    LOGGER.debug(
        "Access token %s\nRefresh token: %s",
        login_resp.access_token,
        login_resp.refresh_token,
    )
    click.echo("Successfully logged in as {}".format(c.eth_address))
    update_config(config_path=config, client=c)


@cli.command(help="Log out of your MythX account")
@config_opt
@staging_opt
def logout(config, staging):
    """Perform a logout action on the API.

    :param config: The configuration file's path
    :param staging: Boolean whether to use the MythX staging deployment
    """
    c = recover_client(config_path=config, staging=staging, exit_on_missing=True)
    if c is None:
        click.echo("You are already logged out.")
        sys.exit(0)
    # delete the credentials storage and logout
    os.remove(config)
    c.logout()
    click.echo("Successfully logged out")


@cli.command(help="Refresh your MythX API token")
@staging_opt
@config_opt
def refresh(staging, config):
    """Perform a refresh action on the API.

    :param staging: Boolean whether to use the MythX staging deployment
    :param config: The configuration file's path
    """
    c = recover_client(config, staging)
    login_resp = c.refresh()
    LOGGER.debug(
        "Access token %s\nRefresh token: %s",
        login_resp.access_token,
        login_resp.refresh_token,
    )
    click.echo("Successfully refreshed tokens for {}".format(c.eth_address))
    update_config(config_path=config, client=c)


@cli.command(help="Get the OpenAPI spec in HTML or YAML format")
@staging_opt
@html_opt
@yaml_opt
def openapi(staging, mode):
    """Return the API's OpenAPI spec data in HTML or YAML format.

    :param staging: Boolean whether to use the MythX staging deployment
    :param mode: The format to return the OpenAPI spec in (HTML or YAML)
    """
    c = Client()  # no auth required
    click.echo(c.openapi(mode).data)


@cli.command(help="Print version information of PythX and the API")
@staging_opt
def version(staging):
    """Return the API's version information as a pretty table.

    :param staging: Boolean whether to use the MythX staging deployment
    """
    c = Client(staging=staging)  # no auth required
    resp = c.version().to_dict()
    data = ((k.title(), v) for k, v in resp.items())
    click.echo(tabulate(data, tablefmt="fancy_grid"))


@cli.command(help="Get the status of an analysis by its UUID")
@config_opt
@staging_opt
@uuid_arg
def status(config, staging, uuid):
    """Return the status of an analysis job as a pretty table.

    :param config: The configuration file's path
    :param staging: Boolean whether to use the MythX staging deployment
    :param uuid: The analysis job's UUID
    """
    c = recover_client(config_path=config, staging=staging)
    resp = c.status(uuid).analysis.to_dict()
    data = ((k, v) for k, v in resp.items())
    click.echo(tabulate(data, tablefmt="fancy_grid"))
    update_config(config_path=config, client=c)


@cli.command(help="Get a greppable overview of submitted analyses")
@config_opt
@staging_opt
@number_opt
def ps(config, staging, number):
    """Return a list of the most recent analyses as a pretty table and exit.

    :param config: The configuration file's path
    :param staging: Boolean whether to use the MythX staging deployment
    :param number: The number of analyses to return
    """
    resp = ps_core(config, staging, number)
    data = [(a.uuid, a.status, a.submitted_at) for a in resp.analyses]
    click.echo(tabulate(data, tablefmt="fancy_grid"))


@cli.command(help="Display the most recent analysis jobs and their status")
@config_opt
@staging_opt
@interval_opt
def top(config, staging, interval):
    """Return a list of the most recent analyses as a pretty table and update it continuously.

    :param config: The configuration file's path
    :param staging: Boolean whether to use the MythX staging deployment
    :param interval: The refresh interval for table updates
    """
    while True:
        resp = ps_core(config, staging, 20)
        click.clear()
        data = [(a.uuid, a.status, a.submitted_at) for a in resp.analyses]
        click.echo(tabulate(data, tablefmt="fancy_grid"))
        time.sleep(interval)


@cli.command(help="Submit a new analysis job based on source code, byte code, or both")
@config_opt
@staging_opt
@bytecode_file_opt
@source_file_opt
@solc_path_opt
def check(config, staging, bytecode_file, source_file, solc_path):
    """

    :param config: The configuration file's path
    :param staging: Boolean whether to use the MythX staging deployment
    :param bytecode_file: A file specifying the bytecode to analyse
    :param source_file: A file specifying the source code to analyse
    :param solc_path: The path to the solc compiler to compile the source code
    """
    c = recover_client(config_path=config, staging=staging)
    if bytecode_file:
        with open(bytecode_file, "r") as bf:
            bytecode_f = bf.read().strip()
        # analyze creation bytecode only
        resp = c.analyze(bytecode=bytecode_f)
    elif source_file:
        with open(source_file, "r") as source_f:
            source_content = source_f.read().strip()
        compiled = compile_from_source(source_file, solc_path=solc_path)
        if len(compiled["contracts"]) > 1:
            click.echo(
                (
                    "The PythX CLI currently does not support sending multiple contracts. "
                    "Please consider using Truffle Security at "
                    "https://github.com/ConsenSys/truffle-security or open a PR to PythX "
                    "at https://github.com/dmuhs/pythx/. :)"
                )
            )
            sys.exit(1)

        for _, contract_data in compiled["contracts"].items():
            bytecode = contract_data["bin"]
            source_map = contract_data["srcmap"]

        sources_dict = copy(compiled["sources"])
        sources_dict[source_file]["source"] = source_content
        resp = c.analyze(
            bytecode=bytecode,
            source_map=source_map,
            source_list=compiled["sourceList"],
            sources=sources_dict,
            solc_version=compiled["version"],
        )
    else:
        click.echo("Please pass a bytecode or a source code file")
        sys.exit(1)

    click.echo("Analysis submitted as job {}".format(resp.analysis.uuid))
    update_config(config_path=config, client=c)


@cli.command(help="Check the detected issues of a finished analysis job")
@config_opt
@staging_opt
@uuid_arg
def report(config, staging, uuid):
    """Retrieve the issue report and resolve the source maps to their file locations.

    :param config: The configuration file's path
    :param staging: Boolean whether to use the MythX staging deployment
    :param uuid: The analysis job's UUID
    """
    c = recover_client(config_path=config, staging=staging)
    resp = c.report(uuid)

    file_to_issue = defaultdict(list)

    for issue in resp.issues:
        source_locs = [loc.source_map.split(":") for loc in issue.locations]
        source_locs = [(int(o), int(l), int(i)) for o, l, i in source_locs]
        for offset, _, file_idx in source_locs:
            if resp.source_list and file_idx > 0:
                filename = resp.source_list[file_idx]
                line, column = get_source_location_by_offset(filename, int(offset))
            else:
                filename = "Unknown"
                line, column = 0, 0
            file_to_issue[filename].append(
                (line, column, issue.swc_title, issue.severity, issue.description_short)
            )

    for filename, data in file_to_issue.items():
        click.echo("Report for {}".format(filename))
        click.echo(
            tabulate(
                data,
                tablefmt="fancy_grid",
                headers=(
                    "Line",
                    "Column",
                    "SWC Title",
                    "Severity",
                    "Short Description",
                ),
            )
        )

    update_config(config_path=config, client=c)
