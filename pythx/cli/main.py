"""Console script for pythx."""
import sys
import os
from os import path, environ
import json
import tempfile
import logging
import time

from pprint import pprint
from pythx.api import Client

import click


logging.basicConfig(level=logging.ERROR)
LOGGER = logging.getLogger("pythx-cli")
DEFAULT_STORAGE_PATH = path.join(tempfile.gettempdir(), ".pythx.json")
CONFIG_KEYS = ("access", "refresh", "username", "password")

staging_opt = click.option(
    "--staging", default=False, is_flag=True, help="Use the MythX staging environment"
)
config_opt = click.option(
    "--config", default=DEFAULT_STORAGE_PATH, help="Path to user credentials JSON file"
)


def parse_config(config_path, tokens_required=False):
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
    return config


def update_config(config_path, username, password, access, refresh):
    with open(config_path, "w+") as config_f:
        json.dump(
            {
                "username": username,
                "password": password,
                "access": access,
                "refresh": refresh,
            },
            config_f,
        )


def recover_client(config_path, staging=False):
    if not path.isfile(config_path):
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
        c = Client(eth_address=eth_address, password=password)
        c.login()
        update_config(
            config_path=config_path,
            username=eth_address,
            password=password,
            access=c.access_token,
            refresh=c.refresh_token,
        )
    else:
        config = parse_config(config_path, tokens_required=True)
        c =  Client(
            eth_address=config["username"],
            password=config["password"],
            access_token=config["access"],
            refresh_token=config["refresh"],
            staging=staging,
        )
    return c


@click.group()
def cli():
    pass


@cli.command(help="Login to your MythX account")
@staging_opt
@config_opt
def login(staging, config):
    c = recover_client(config, staging)
    login_resp = c.login()
    LOGGER.debug(
        "Access token %s\nRefresh token: %s",
        login_resp.access_token,
        login_resp.refresh_token,
    )


@cli.command(help="Log out of your MythX account")
@config_opt
@staging_opt
def logout(config, staging):
    c = recover_client(config_path=config, staging=staging)
    # delete the credentials storage and logout
    os.remove(config)
    c.logout()


@cli.command(help="Get the OpenAPI spec in HTML or YAML format")
@staging_opt
@click.option("--html", "mode", flag_value="html", help="Get the HTML OpenAPI spec")
@click.option("--yaml", "mode", flag_value="yaml", default=True, help="Get the YAML OpenAPI spec")
def openapi(staging, mode):
    c = Client()  # no auth required
    click.echo(c.openapi(mode).data)


@cli.command(help="Print version information of PythX and the API")
@staging_opt
def version(staging):
    c = Client()  # no auth required
    resp = c.version()
    for name, value in (
        ("API", resp.api_version),
        ("Maru", resp.maru_version),
        ("Mythril", resp.mythril_version),
        ("Maestro", resp.maestro_version),
        ("Harvey", resp.harvey_version),
        ("Hash", resp.hashed_version)
    ):
        click.echo("{}: {}".format(name, value))


@cli.command(help="Get the status of an analysis by its UUID")
@config_opt
@staging_opt
@click.argument("uuid", type=click.UUID)
def status(config, staging, uuid):
    c = recover_client(config_path=config, staging=staging)
    resp = c.status(uuid).analysis
    for name, value in (
        ("UUID", resp.uuid),
        ("API Version", resp.api_version),
        ("Mythril", resp.mythril_version),
        ("Maestro", resp.maestro_version),
        ("Maru", resp.maru_version),
        ("Queue Time", resp.queue_time),
        ("Run Time", resp.run_time),
        ("Status", resp.status.title()),
        ("Submitted By", resp.submitted_by),
        ("Submitted At", resp.submitted_at),

    ):
        click.echo("{}: {}".format(name, value))


@cli.command(help="Get a greppable overview of submitted analyses")
@config_opt
@staging_opt
@click.option(
    "--number",
    default=20,
    type=click.IntRange(min=1, max=100),
    help="The number of most recent analysis jobs to display",
)
def ps(config, staging, number):
    resp = ps_core(config, staging, number)
    click.echo("Got {} analyses:".format(resp.total))
    pprint(resp.to_dict())


def ps_core(config, staging, number):
    c = recover_client(config_path=config, staging=staging)
    resp = c.analysis_list()
    return resp


@cli.command(help="Display the most recent analysis jobs and their status")
@config_opt
@staging_opt
@click.option("--interval", default=5, type=click.INT, help="Refresh interval")
def top(config, staging, interval):
    while True:
        click.clear()
        resp = ps_core(config=config, staging=staging, number=20)
        pprint(resp.to_dict())
        time.sleep(interval)


@cli.command(help="Submit a new analysis job based on source code, byte code, or both")
@config_opt
@staging_opt
@click.option(
    "--bytecode", "-b", type=click.STRING, default=None, help="Analysis job creation byte code"
)
@click.option(
    "--source", "-s", type=click.STRING, default=None,help="Analysis job Solidity source code"
)
@click.option("--bytecode-file", "-bf", type=click.Path(exists=True), default=None, help="Path to file containing creation bytecode")
@click.option("--source-file", "-sf", type=click.Path(exists=True), default=None, help="Path to file containing Solidity source code")
def check(config, staging, bytecode, source, bytecode_file, source_file):
    c = recover_client(config_path=config, staging=staging)
    bytecode_f = bytecode if bytecode else None
    sources_f = {"cli-src.sol": {"source": source}} if source else {}
    if bytecode_file:
        with open(bytecode_file, "r") as bf:
            bytecode_f = bf.read().strip()  # CLI arg bytecode takes preference
    if source_file:
        with open(source_file, "r") as sf:
            sources_f = {source_file: {"source": sf.read().strip()}}

    resp = c.analyze(
        bytecode=bytecode_f,
        sources=sources_f
    )
    click.echo("Submitted analysis: {}".format(resp.analysis.uuid))


@cli.command(help="Check the detected issues of a finished analysis job")
@config_opt
@staging_opt
@click.argument("uuid", type=click.STRING)
def report(config, staging, uuid):
    c = recover_client(config_path=config, staging=staging)
    resp = c.report(uuid)
    pprint(resp.to_dict())
