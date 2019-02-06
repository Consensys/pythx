import dateutil.parser
from datetime import datetime


def deserialize_api_timestamp(timestamp_str: str):
    return dateutil.parser.parse(timestamp_str)

def serialize_api_timestamp(ts_obj: datetime):
    ts_str = ts_obj.strftime('%Y-%m-%dT%H:%M:%S.%f')
    # chop off last 3 digits because JS
    return  ts_str[:-3] + "Z"