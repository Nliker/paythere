import sys,os
sys.path.append((os.path.dirname(os.path.abspath(os.path.dirname(__file__)))))

from main import create_app
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine,text
from config import make_conf_dict
import bcrypt
import jwt
from datetime import datetime,timedelta
from response import *

conf=make_conf_dict()

database=create_engine(f"mysql+mysqlconnector://{conf.user}:{conf.password}@{conf.host}:{conf.port}/{conf.database}?charset=utf8")

@pytest.fixture(scope='session')
def client():
    app=create_app()
    client=TestClient(app)

    return client

def generate_token(user_id):
    jwt_expire_time=timedelta(seconds=conf.jwt_expire_time)
    utc_time_now=datetime.utcnow()
    access_token_expire=utc_time_now+jwt_expire_time

    payload={
            'user_id':user_id,
            'exp':access_token_expire,
            'iat':utc_time_now
    }

    access_token=jwt.encode(payload,conf.jwt_secret_key,'HS256')
    return access_token

def generate_hashed_password(password):
    hash_password=bcrypt.hashpw(
        password.encode('utf-8'),
        bcrypt.gensalt()
    )
    return hash_password
    

#가입이 후 로그인 안 한 유저
class user1:
    user_id=1
    phone_number="01011111111"
    password="11111111"
    hash_password=generate_hashed_password("11111111")

#가입 후 로그인 한 유저
class user2:
    user_id=2
    phone_number="01022222222"
    password="22222222"
    access_token=generate_hashed_password("22222222")
    
    
    
def setup_funtion():
    with database.connect() as conn:
        conn.execute(
            text(
                """
                    truncate users
                """
            )
        )
        conn.execute(
            text(
                """
                    truncate products
                """
            )
        )
        conn.execute(
            text(
                """
                    truncate products_initial
                """
            )
        )
        conn.execute(
            text(
                """
                    truncate tokens
                """
            )
        )
        new_users=[{
                        'id':user1.user_id,
                        'phone_number':user1.phone_number,
                        'hashed_password':user1.hash_password
                    },
                    {
                        'id':user2.user_id,
                        'phone_number':user2.phone_number,
                        'hashed_password':user2.hash_password
                    }
        ]
        new_tokens=[{
            'access_token':user2.access_token
        }]
        conn.execute(
            text(
                """
                    insert into users(id,phone_number,hashed_password) values(:id,:phone_number,:hashed_password)
                """
                ),new_users
        )
        conn.execute(
            text(
                """
                    insert into tokens(access_token) values(:access_token)
                """
                ),new_tokens
        )
    
def teardown_function():
    with database.connect() as conn:
        conn.execute(
            text(
                """
                    truncate users
                """
            )
        )
        conn.execute(
            text(
                """
                    truncate products
                """
            )
        )
        conn.execute(
            text(
                """
                    truncate products_initial
                """
            )
        )
        conn.execute(
            text(
                """
                    truncate tokens
                """
            )
        )
    
def test_ping(client):
    resp=client.get('/ping')

    assert resp.status_code==Get_200.status_code
