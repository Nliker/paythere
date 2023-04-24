from .api_response import *
def make_http_response_json(status,data):
    return {
        "meta":
            {
                "code":status.status_code,
                "message":status.status_code
            },
        "data":data
    }

    