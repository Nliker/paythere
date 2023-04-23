from .sql_exception import *
from .service_exception import *
from .api_exception import *

from fastapi import HTTPException

def make_http_error(error):
    raise HTTPException(status_code=error.status_code, detail=error.__str__())