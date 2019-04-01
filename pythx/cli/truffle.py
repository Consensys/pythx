"""This module contains functions to submit Truffle projects to MythX."""

from pythx.cli.logger import LOGGER
from glob import glob
from os import path


def find_artifacts(project_dir):
    """Look for a Truffle build folder and return all relevant JSON artifacts.

    This function will skip the Migrations.json file and return all other paths
    under .../build/contracts/.
    """

    output_pattern = path.join(project_dir, "build", "contracts", "*.json")
    for json_file in glob(output_pattern):
        if json_file.endswith("Migrations.json"):
            LOGGER.debug("Skipping built migrations file")
            continue

        yield json_file
