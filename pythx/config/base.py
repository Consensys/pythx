class PythXConfig(dict):
    def __init__(self):
        self["endpoints"] = {
            "base": "",
            "auth": {"login": "", "logout": "", "refresh": ""},
            "analysis": {"list": "", "submission": "", "status": "", "issues": ""},
            "openapi": {"html", "yaml"},
            "version": "",
        }
