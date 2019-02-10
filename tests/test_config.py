from pythx import config
from pythx.config.base import PythXConfig

import pytest


TEST_KEY = "test_key"
TEST_VALUE = ("test_method", "test_value")


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


def test_validate():
    config.validate()
    config["endpoints"]["foo"] = "bar"  # not dict or tuple
    with pytest.raises(TypeError):
        config.validate()
