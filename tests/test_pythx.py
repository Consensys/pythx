import pytest
from click.testing import CliRunner

from pythx.cli import main


@pytest.mark.parametrize(
    "command_name",
    ["check", "login", "logout", "openapi", "ps", "status", "top", "version"],
)
def test_subcommands(command_name):
    runner = CliRunner()
    result = runner.invoke(main.cli)
    assert command_name in result.output
    result = runner.invoke(main.cli, ["--help"])
    assert command_name in result.output
