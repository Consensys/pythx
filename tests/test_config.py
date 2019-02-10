from pythx import config
from pythx.config.base import PythXConfig


TEST_KEY = "test_key"
TEST_VALUE = "test_value"


def test_base_class():
    assert type(config) == PythXConfig
    assert isinstance(config, dict)


def test_endpoints():
    assert config.get("endpoints") is not None


def test_add_remove_key():
    config[TEST_KEY] = TEST_VALUE
    assert config.get(TEST_KEY) == TEST_VALUE
    del config[TEST_KEY]
    assert config.get(TEST_KEY) is None
