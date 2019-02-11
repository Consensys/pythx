from pythx.core.request import models as reqmodels


class PythXConfig(dict):
    def __init__(self):
        self["endpoints"] = {
            "production": "https://api.mythx.io/v1/",
            "staging": "https://staging.api.mythx.io/v1/",
        }
