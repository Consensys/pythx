import json
from pathlib import Path
from mythx_models.response import DetectedIssuesResponse


def get_test_case(path: str, obj=None):
    with open(str(Path(__file__).parent / path)) as f:
        dict_data = json.load(f)

    if obj is None:
        return dict_data

    if obj is DetectedIssuesResponse and type(dict_data) is list:
        return obj(issue_reports=dict_data)
    else:
        return obj(**dict_data)


def generate_request_dict(req):
    return {
        "method": req.method,
        "payload": req.payload,
        "params": req.parameters,
        "headers": req.headers,
        "url": "https://test.com/" + req.endpoint,
    }
