from .sql_exception import *
from .service_exception import *
from .api_exception import *
from .validation import *

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
    "PasswordNotAuthorized":True,
    "UserIdNotExists":True,
    "ProductIdNotExists":True,
    "ProductWasDeleted":True,
    "ProductUpdatFailed":True,
    "ProductNotAuthorizedByUser":True,
    "UserLogouted":True,
    "PhoneNumberLength":True,
    "PasswordLength":True,
    "NameKorean":True,
    "CategoryLength":True,
    "NameLength":True,
    "PriceRange":True,
    "DescriptionLength":True,
    "BarcodeLength":True,
    "Size":True,
    "ExpireationDate":True,
    "PhoneNumberType":True
}