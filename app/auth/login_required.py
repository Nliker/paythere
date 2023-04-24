import sys,os
sys.path.append((os.path.dirname(os.path.abspath(os.path.dirname(__file__)))))
from fastapi import Header,HTTPException
from config import make_conf_dict
import jwt
from typing import Union
import exception

conf=make_conf_dict()

async def verify_token(access_token: Union  [str, None]=Header(default=None)):
    if access_token is not None:
        try:
            payload=jwt.decode(access_token,conf.jwt_secret_key,"HS256")
        except:
            print("유효하지 않은 토큰")
            error=exception.BrokenToken()
            raise HTTPException(status_code=error.status_code,detail=error.__str__())
        if 'user_id' not in payload and type(payload['user_id']) !=type(1):
            print("내용이 유효하지 않은 토큰")
            error=exception.WrongToken()
            raise HTTPException(status_code=error.status_code,detail=error.__str__())
    else:
        error=exception.TokenNotExists()
        raise HTTPException(status_code=error.status_code,detail=error.__str__())
    
    return payload['user_id']
