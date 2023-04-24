from .sql_exception import *
from .service_exception import *
from .api_exception import *

def make_http_error(status_code,detail):
    return {
        "meta":
            {
                "code":status_code,
                "message":detail
            },
        "data":None
    }


exceptions_dict={
    "PhoneNumberExists":True,
    "UserWasDeleted":True,
    "DatabaseError":True,
    "PhoneNumberNotExists":True,
    "PasswordNotAuthorized":True
}