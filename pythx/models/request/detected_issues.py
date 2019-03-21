from pythx.models.request.analysis_status import AnalysisStatusRequest


class DetectedIssuesRequest(AnalysisStatusRequest):
    def __init__(self, uuid: str):
        super().__init__(uuid)
        self.uuid = uuid

    @property
    def endpoint(self):
        return "v1/analyses/{}/issues".format(self.uuid)

    @property
    def method(self):
        return "GET"

    @property
    def parameters(self):
        return {}
