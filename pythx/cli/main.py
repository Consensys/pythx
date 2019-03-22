"""Console script for pythx."""
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
    """

    :param config_path:
    :param tokens_required:
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
    """

    :param config_path:
    :param client:
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
    """

    :param config_path:
    :param staging:
    :param exit_on_missing:
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
    """

    :param config:
    :param staging:
    :param number:
    :return:
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
    # todo: pagination if too few
    resp.analyses = resp.analyses[: number + 1]
    update_config(config_path=config, client=c)
    return resp


def get_source_location_by_offset(filename, offset):
    """

    :param filename:
    :param offset:
    :return:
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
    """

    :param source_path:
    :param solc_path:
    :return:
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
    """

    """
    pass  # pragma: no cover


@cli.command(help="Login to your MythX account")
@staging_opt
@config_opt
def login(staging, config):
    """

    :param staging:
    :param config:
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
    """

    :param config:
    :param staging:
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
    """

    :param staging:
    :param config:
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
    """

    :param staging:
    :param mode:
    """
    c = Client()  # no auth required
    click.echo(c.openapi(mode).data)


@cli.command(help="Print version information of PythX and the API")
@staging_opt
def version(staging):
    """

    :param staging:
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
    """

    :param config:
    :param staging:
    :param uuid:
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
    """

    :param config:
    :param staging:
    :param number:
    """
    resp = ps_core(config, staging, number)
    data = [(a.uuid, a.status, a.submitted_at) for a in resp.analyses]
    click.echo(tabulate(data, tablefmt="fancy_grid"))


@cli.command(help="Display the most recent analysis jobs and their status")
@config_opt
@staging_opt
@interval_opt
def top(config, staging, interval):
    """

    :param config:
    :param staging:
    :param interval:
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

    :param config:
    :param staging:
    :param bytecode_file:
    :param source_file:
    :param solc_path:
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
    """

    :param config:
    :param staging:
    :param uuid:
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
