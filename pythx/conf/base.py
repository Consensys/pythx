"""This module contains the base PythX config instantiated in the module's __init__ file."""


class PythXConfig(dict):
    """The global configuration object.

    The PythX global configuration is accessible by all PythX modules and allows each component
    to exhibit the same behaviour while keeping each module isolated. By default, the config
    object contains the relevant endpoints for the MythX API production and staging deployments
    to make it easier for developers to switch between the two.

    The config object is a subclass of a standard Python dictionary, so it can be used just like
    that by developers.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self["endpoints"] = {
            "production": "https://api.mythx.io/",
            "staging": "https://staging.api.mythx.io/",
        }
