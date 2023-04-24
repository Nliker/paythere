from .api_response import *
def make_http_response_json(success_response,data):
    return {
        "meta":
            {
                "code":success_response.status_code,
                "message":success_response.message
            },
        "data":data
    }

    