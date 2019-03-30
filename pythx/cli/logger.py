"""This module contains the CLI logger."""

import logging
from os import environ

if environ.get("PYTHX_DEBUG") is not None:
    logging.basicConfig(level=logging.DEBUG)
else:
    logging.basicConfig(level=logging.ERROR)

LOGGER = logging.getLogger("pythx-cli")
