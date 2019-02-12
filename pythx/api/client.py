from pythx.api.handler import APIHandler


class Client:
    def __init__(
        self,
        eth_address: str,
        password: str,
        handler: APIHandler = None,
        access_token: str = None,
        refresh_token: str = None,
    ):
        self.eth_address = eth_address
        self.password = password
        self.handler = handler or APIHandler()
        self.access_token = access_token
        self.refresh_token = refresh_token

    def login(self):
        pass

    def logout(self):
        pass

    def refresh(self):
        pass

    def analysis_list(self):
        pass

    def analyze(self):
        pass

    def status(self):
        pass

    def analysis_ready(self):
        pass

    def report(self):
        pass

    def openapi(self):
        pass

    def version(self):
        pass
