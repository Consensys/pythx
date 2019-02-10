class PythXConfig(dict):
    def __init__(self):
        self["endpoints"] = {
            "production": {
                "base": "https://api.mythx.io/v1/",
                "auth": {
                    "login": " /auth/login",
                    "logout": "/auth/logout",
                    "refresh": "/auth/refresh",
                },
                "analysis": {
                    "list": "/analyses",
                    "submission": "/analyses",
                    "status": "/analyses/{uuid}",
                    "issues": "/analyses/{uuid}/issues",
                },
                "openapi": {"html": "/openapi", "yaml": "/openapi.yaml"},
                "version": " /version",
            },
            "staging": {
                "base": "https://staging.api.mythx.io/v1/",
                "auth": {
                    "login": " /auth/login",
                    "logout": "/auth/logout",
                    "refresh": "/auth/refresh",
                },
                "analysis": {
                    "list": "/analyses",
                    "submission": "/analyses",
                    "status": "/analyses/{uuid}",
                    "issues": "/analyses/{uuid}/issues",
                },
                "openapi": {"html": "/openapi", "yaml": "/openapi.yaml"},
                "version": " /version",
            },
        }
