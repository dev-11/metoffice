import json
from datetime import datetime, date
from decimal import Decimal

def json_default(obj):
    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    if isinstance(obj, Decimal):
        return float(obj)
    raise TypeError

def lambda_handler_wrapper(handler):
    def wrapped(event, context):
        result = handler(event, context)
        return json.dumps(result, default=json_default)

    return wrapped
