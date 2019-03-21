import pytest

from pythx import config
from pythx.conf.base import PythXConfig

TEST_KEY = "test_key"
TEST_VALUE = ("test_method", "test_value")


def test_base_class():
    assert type(config) == PythXConfig
    assert isinstance(config, dict)


def test_endpoints_keys():
    endpoints = config.get("endpoints")
    assert endpoints is not None
    assert endpoints.get("staging") is not None
    assert endpoints.get("production") is not None


def test_add_remove_key():
    config[TEST_KEY] = TEST_VALUE
    assert config.get(TEST_KEY) == TEST_VALUE
    del config[TEST_KEY]
    assert config.get(TEST_KEY) is None
