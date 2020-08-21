import json


def sse(data, event="", dumps=json.dumps):
    message = ""
    if event:
        message += f"event: {event}\n"
    message += f"data: {dumps(data)}\n\n"
    return message
