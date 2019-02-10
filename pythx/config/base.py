class PythXConfig(dict):
    def __init__(self):
        self["endpoints"] = {
            "production": {
                "base": "https://api.mythx.io/v1/",
                "auth": {
                    "login": ("POST", "/auth/login"),
                    "logout": ("POST", "/auth/logout"),
                    "refresh": ("POST", "/auth/refresh"),
                },
                "analysis": {
                    "list": ("GET", "/analyses"),
                    "submission": ("POST", "/analyses"),
                    "status": ("GET", "/analyses/{uuid}"),
                    "issues": ("GET", "/analyses/{uuid}/issues"),
                },
                "openapi": {"html": ("GET", "/openapi"), "yaml": ("GET", "/openapi.yaml")},
                "version": ("GET", "/version"),
            },
            "staging": {
                "base": "https://staging.api.mythx.io/v1/",
                "auth": {
                    "login": ("POST", "/auth/login"),
                    "logout": ("POST", "/auth/logout"),
                    "refresh": ("POST", "/auth/refresh"),
                },
                "analysis": {
                    "list": ("GET", "/analyses"),
                    "submission": ("POST", "/analyses"),
                    "status": ("GET", "/analyses/{uuid}"),
                    "issues": ("GET", "/analyses/{uuid}/issues"),
                },
                "openapi": {"html": ("GET", "/openapi"), "yaml": ("GET", "/openapi.yaml")},
                "version": ("GET", "/version"),
            },
        }

    def validate(self):
        for key, value in self["endpoints"].items():
            if key != "base" and type(value) not in (dict, tuple):
                raise TypeError("Config pair ({},{})) is not of type dict or tuple")
