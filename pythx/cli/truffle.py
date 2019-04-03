"""This module contains functions to submit Truffle projects to MythX."""

from glob import glob
from os import path


def find_artifacts(project_dir):
    """Look for a Truffle build folder and return all relevant JSON artifacts.

    This function will skip the Migrations.json file and return all other paths
    under <project-dir>/build/contracts/.
    """

    output_pattern = path.join(project_dir, "build", "contracts", "*.json")
    artifact_files = list(glob(output_pattern))

    if not artifact_files:
        return None

    return [f for f in artifact_files if not f.endswith("Migrations.json")]
