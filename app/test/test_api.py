import sys,os
sys.path.append((os.path.dirname(os.path.abspath(os.path.dirname(__file__)))))

from main import create_app
import copy
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine,text
from sqlalchemy.sql import text
from config import make_conf_dict
import bcrypt
import jwt
from datetime import datetime,timedelta
from response import *

conf=make_conf_dict()
db=create_engine(f"mysql+mysqlconnector://{conf.user}:{conf.password}@{conf.host}:{conf.port}/{conf.database}?charset=utf8")


@pytest.fixture(scope="session")
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


#로그아웃을 한 유저
class User1:
    user_id=1
    phone_number="01011111111"
    password="11111111"
    hashed_password=generate_hashed_password("11111111")

#가입 후 로그인 한 유저
class User2:
    user_id=2
    phone_number="01022222222"
    password="22222222"
    hashed_password=generate_hashed_password("22222222")
    access_token=generate_token(user_id)

#2번 유저 소유의 상품
class Product1:
    product_id=1
    user_id=User2.user_id
    category="간식"
    net_price=3000.00
    cost_price=2000.00
    name="차카니"
    description="매콤하고 가격이 싸서 가성비좋습니다."
    barcode= "1234567891234"
    expiration_date="2023-05-20"
    size= "small"
    
 
#테스트 시작시마다 DB를 초기화 하고 데이터를 삽입합니다.
def setup_function():
    with db.connect() as conn:
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
                                'id':User1.user_id,
                                'phone_number':User1.phone_number,
                                'hashed_password':User1.hashed_password
                            },
                            {
                                'id':User2.user_id,
                                'phone_number':User2.phone_number,
                                'hashed_password':User2.hashed_password
                            }
                ]
        new_tokens=[{
                    'access_token':User2.access_token
                }]
        new_products=[{
            "id":Product1.product_id,
            "user_id":Product1.user_id,
            "category":Product1.category,
            "net_price":Product1.net_price,
            "cost_price":Product1.cost_price,
            "name":Product1.name,
            "description":Product1.description,
            "barcode":Product1.barcode,
            "expiration_date":Product1.expiration_date,
            "size": Product1.size
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
                            insert into products(id,user_id,category,net_price,cost_price,name,description,barcode,expiration_date,size) 
                            values(:id,:user_id,:category,:net_price,:cost_price,:name,:description,:barcode,:expiration_date,:size)
                        """
                        ),new_products
                )
        conn.execute(
                    text("""insert into tokens(access_token) values(:access_token)"""),new_tokens
                    )
        conn.commit()

# 테스트 종료시마다 DB를 초기화 합니다.
def teardown_function():
    with db.connect() as conn:
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
        conn.commit()

def get_data(response):
    return response["data"]

def test_ping(client):
    resp=client.get('/ping')

    assert resp.status_code==Get_200.status_code
    
#회원가입의 유효성 테스트
def test_payment_fail_post_signup(client):
    #핸드폰번호가 영어일 경우
    data={
        "phone_number":"english",
        "password":"12345678"
    }
    resp=client.post('/users/sign_up',json=(data))
    assert resp.status_code==400
    
    #핸드폰번호가 11자리가 아닐경우
    data={
        "phone_number":"0101234567890",
        "password":"12345678"
    }
    resp=client.post('/users/sign_up',json=(data))
    assert resp.status_code==400

    #핸드폰번호가 8이상 16자리 이하가 아닐경우
    data={
        "phone_number":"01012345678",
        "password":"1234"
    }
    resp=client.post('/users/sign_up',json=(data))
    assert resp.status_code==400

    #이미 가입된 유저가 존재할 경우
    data={
        "phone_number":User1.phone_number,
        "password":User1.password
    }
    assert resp.status_code==400

#회원가입 테스트
def test_post_signup(client):
    data={
        "phone_number":"01012345678",
        "password":"12345678"
    }
    resp=client.post('/users/sign_up',json=(data))

    assert resp.status_code==Created_201.status_code

#로그인 실패 테스트
def test_fail_post_login(client):
    #존재하지 않는 유저일 경우
    data={
        "phone_number":"01099999999",
        "password":"99999999"
    }
    resp=client.post('/users/login',json=(data))
    assert resp.status_code==401

#로그인 진행 테스트
def test_post_login(client):
    data={
        "phone_number":User1.phone_number,
        "password":User1.password
    }
    resp=client.post('/users/login',json=(data))
    assert resp.status_code==Created_201.status_code

    resp_data=get_data(resp.json())
    assert "access_token" in resp_data

#로그아웃 실패 진행테스트
def test_fail_post_user_logout(client):    
    #로그아웃을 했던 유저가 다시 로그아웃
    resp=client.post('/users/logout',
                    headers={'access-token':User2.access_token})
    assert resp.status_code==Created_201.status_code
    
    resp=client.post('/users/logout',
                    headers={'access-token':User2.access_token})
    assert resp.status_code==401

#로그아웃을 한 유저의 서비스 실패테스트
def test_fail_with_logut(client):
    resp=client.post('/users/logout',
                    headers={'access-token':User2.access_token})
    assert resp.status_code==Created_201.status_code
    
    resp=client.get('/users/my')
    assert resp.status_code==401
    
    resp=client.get('/products')
    assert resp.status_code==401
    
    data={
            "category": "음료",
            "net_price": 3000,
            "cost_price": 2000,
            "name": "우유라떼",
            "description": "고소하고 맛있습니다.",
            "barcode": "1234567891234",
            "expiration_date": "2023-05-20",
            "size": "small"
        }

    
    resp=client.post('/products',json=(data),headers={'access-token':User2.access_token})
    assert resp.status_code==401
    
    resp=client.get('/products/1',headers={'access-token':User2.access_token})
    assert resp.status_code==401
    
    resp=client.delete('/products/1',headers={'access-token':User2.access_token})
    assert resp.status_code==401
    
    resp=client.get('/search/products?name=카페라떼',headers={'access-token':User2.access_token})
    assert resp.status_code==401

#유저의 정보 불러오오기
def test_get_my(client):
    #가입 후 로그인 한 유저로 불러오기
    resp=client.get('/users/my',
                    headers={'access-token':User2.access_token})
    assert resp.status_code==Get_200.status_code

    data=get_data(resp.json())
    assert data=={
        'user':{
            "phone_number": User2.phone_number,
            "id": User2.user_id,
            "created_at": data['user']['created_at']
        }
    }



#상품조회 실패 테스트
def test_fail_get_product(client):
    #존재하지 않는 상품일 경우
    resp=client.get('/products/9999',headers={'access-token':User2.access_token})
    assert resp.status_code==404
    
    #자신의 소유가 아닌 상품일 경우
    data={
        "phone_number":User1.phone_number,
        "password":User1.password
    }
    resp=client.post('/users/login',json=(data))
    assert resp.status_code==Created_201.status_code

    resp_data=get_data(resp.json())
    assert "access_token" in resp_data

    user1_access_token=resp_data["access_token"]
    resp=client.get(f'/products/{Product1.product_id}',headers={'access-token':user1_access_token})
    assert resp.status_code==403

#상품조회 테스트
def test_get_product(client):
    resp=client.get(f'/products/{Product1.product_id}',headers={'access-token':User2.access_token})
    assert resp.status_code==Get_200.status_code

    resp_data=get_data(resp.json())
    assert resp_data=={
        "product": {
            "category": Product1.category,
            "net_price": Product1.net_price,
            "cost_price": Product1.cost_price,
            "name": Product1.name,
            "description": Product1.description,
            "barcode": Product1.barcode,
            "expiration_date": Product1.expiration_date,
            "size": Product1.size,
            "id": Product1.product_id,
            "created_at":resp_data["product"]["created_at"]
        }
    }

#상품 등록 테스트
def test_post_products(client):
    data={
            "category": "음료",
            "net_price": 3000,
            "cost_price": 2000,
            "name": "우유라떼",
            "description": "고소하고 맛있습니다.",
            "barcode": "1234567891234",
            "expiration_date": "2023-05-20",
            "size": "small"
        }
    #로그인 한 유저가 상품 등록
    
    resp=client.post('/products',json=(data),headers={'access-token':User2.access_token})
    assert resp.status_code==Created_201.status_code
    
    resp_data=get_data(resp.json())
    created_product_id=resp_data['product']['id']

    resp=client.get(f'/products/{created_product_id}',headers={'access-token':User2.access_token})
    assert resp.status_code==200
    resp_data=get_data(resp.json())
    assert resp_data=={
        "product":{
            "id":created_product_id,
            "category": "음료",
            "net_price": 3000,
            "cost_price": 2000,
            "name": "우유라떼",
            "description": "고소하고 맛있습니다.",
            "barcode": "1234567891234",
            "expiration_date": "2023-05-20",
            "size": "small",
            "created_at":resp_data["product"]["created_at"]
        }
    }

#페이지 기반 자신의 상품 리스트조회 테스트
def test_get_products(client):
    data={
            "category": "음료",
            "net_price": 3000,
            "cost_price": 2000,
            "name": "우유라떼",
            "description": "고소하고 맛있습니다.",
            "barcode": "1234567891234",
            "expiration_date": "2023-05-20",
            "size": "small"
        }
    page=1
    data_list=[]
    for i in range(15):
        sample_data=copy.deepcopy(data)
        sample_data["net_price"]=i*1000
        data_list.append(sample_data)
    
    for sample_data in data_list:
        resp=client.post('/products',json=(sample_data),headers={'access-token':User2.access_token})
        assert resp.status_code==Created_201.status_code

    resp=client.get(f'/products?page={page}',headers={'access-token':User2.access_token})
    assert resp.status_code==Get_200.status_code
    
    resp_data=get_data(resp.json())
    assert len(resp_data["products"])==page*10 

#상품등록의 유효성 테스트
def test_fail_payment_post_products(client):
    data={
            "category": "음료",
            "net_price": 3000,
            "cost_price": 2000,
            "name": "우유라떼",
            "description": "고소하고 맛있습니다.",
            "barcode": "1234567891234",
            "expiration_date": "2023-05-20",
            "size": "small"
        }
    #카테고리 글자 수 제한
    category_invalid_data=copy.deepcopy(data)
    category_invalid_data["category"]="a"*500
    resp=client.post('/products',json=(category_invalid_data),headers={'access-token':User2.access_token})
    assert resp.status_code==400

    #정가 가격제한
    net_price_invalid_data=copy.deepcopy(data)
    net_price_invalid_data["net_price"]=10000000000
    resp=client.post('/products',json=(net_price_invalid_data),headers={'access-token':User2.access_token})
    assert resp.status_code==400
    
    #원가 가격제한
    cost_price_invalid_data=copy.deepcopy(data)
    cost_price_invalid_data["cost_price"]=10000000000
    resp=client.post('/products',json=(cost_price_invalid_data),headers={'access-token':User2.access_token})
    assert resp.status_code==400
    
    #이름 완전 한글음이 아닌건 제한
    name_invalid_data=copy.deepcopy(data)
    name_invalid_data["name"]="ㅋ피라떼"
    resp=client.post('/products',json=(name_invalid_data),headers={'access-token':User2.access_token})
    assert resp.status_code==400

    #설명 글자 수 제한
    description_invalid_data=copy.deepcopy(data)
    description_invalid_data["description"]="a"*500
    resp=client.post('/products',json=(description_invalid_data),headers={'access-token':User2.access_token})
    assert resp.status_code==400
    
    #바코드 13자리 아닌 것 제한
    barcode_invalid_data=copy.deepcopy(data)
    barcode_invalid_data["barcode"]="a"*5
    resp=client.post('/products',json=(barcode_invalid_data),headers={'access-token':User2.access_token})
    assert resp.status_code==400

    #3000년 이후인 것 제한
    expiration_date_invalid_data=copy.deepcopy(data)
    expiration_date_invalid_data["expiration_date"]="9999-09-09"
    resp=client.post('/products',json=(expiration_date_invalid_data),headers={'access-token':User2.access_token})
    assert resp.status_code==400
    
    #사이즈 small,medium,large 아닌 것 제한
    size_date_invalid_data=copy.deepcopy(data)
    size_date_invalid_data["size"]="superextra"
    resp=client.post('/products',json=(size_date_invalid_data),headers={'access-token':User2.access_token})
    assert resp.status_code==400

#상품업데이트의 유효성 테스트
def test_fail_payment_put_products(client):
    data={}

    data["category"]="a"*500
    resp=client.put(f'/products/{Product1.product_id}',json=(data),headers={'access-token':User2.access_token})
    assert resp.status_code==400

    data["net_price"]=10000000000
    resp=client.put(f'/products/{Product1.product_id}',json=(data),headers={'access-token':User2.access_token})
    assert resp.status_code==400

    data["cost_price"]=10000000000
    resp=client.put(f'/products/{Product1.product_id}',json=(data),headers={'access-token':User2.access_token})
    assert resp.status_code==400

    data["name"]="ㅋ피라떼"
    resp=client.put(f'/products/{Product1.product_id}',json=(data),headers={'access-token':User2.access_token})
    assert resp.status_code==400

    data["description"]="a"*500
    resp=client.put(f'/products/{Product1.product_id}',json=(data),headers={'access-token':User2.access_token})
    assert resp.status_code==400

    data["barcode"]="a"*5
    resp=client.put(f'/products/{Product1.product_id}',json=(data),headers={'access-token':User2.access_token})
    assert resp.status_code==400

    data["expiration_date"]="9999-09-09"
    resp=client.put(f'/products/{Product1.product_id}',json=(data),headers={'access-token':User2.access_token})
    assert resp.status_code==400

    data["size"]="superextra"
    resp=client.put(f'/products/{Product1.product_id}',json=(data),headers={'access-token':User2.access_token})
    assert resp.status_code==400

#상품업데이트 실패 테스트
def test_fail_put_products(client):
    update_data={
        "category":"주류",
        "net_price":4000
    }
    #존재하지 않는 상품일 경우
    resp=client.put('/products/9999',json=(update_data),headers={'access-token':User2.access_token})
    assert resp.status_code==404
    
    #자신의 상품이 아닐 경우
    data={
        "phone_number":User1.phone_number,
        "password":User1.password
    }
    resp=client.post('/users/login',json=(data))
    assert resp.status_code==Created_201.status_code

    resp_data=get_data(resp.json())
    assert "access_token" in resp_data

    user1_access_token=resp_data["access_token"]
    resp=client.put(f'/products/{Product1.product_id}',json=(update_data),headers={'access-token':user1_access_token})
    assert resp.status_code==403

#상품의업데이트 테스트
def test_put_products(client):
    update_data={
        "category":"주류",
        "net_price":4000.00
    }
    resp=client.put(f'/products/{Product1.product_id}',json=(update_data),headers={'access-token':User2.access_token})
    assert resp.status_code==Created_201.status_code
    
    resp=client.get(f'/products/{Product1.product_id}',headers={'access-token':User2.access_token})
    assert resp.status_code==Get_200.status_code

    resp_data=get_data(resp.json())
    assert resp_data=={
        "product": {
            "category": update_data["category"],
            "net_price": update_data["net_price"],
            "cost_price": Product1.cost_price,
            "name": Product1.name,
            "description": Product1.description,
            "barcode": Product1.barcode,
            "expiration_date": Product1.expiration_date,
            "size": Product1.size,
            "id": Product1.product_id,
            "created_at":resp_data["product"]["created_at"]
        }
    }

#상품삭제 실패 테스트
def test_fail_delete_product(client):
    #존재하지 않는 상품일 경우
    resp=client.delete('/products/9999',headers={'access-token':User2.access_token})
    assert resp.status_code==404
    
    #자신의 상품이 아닐 경우
    data={
        "phone_number":User1.phone_number,
        "password":User1.password
    }
    resp=client.post('/users/login',json=(data))
    assert resp.status_code==Created_201.status_code

    resp_data=get_data(resp.json())
    assert "access_token" in resp_data

    user1_access_token=resp_data["access_token"]
    resp=client.delete(f'/products/{Product1.product_id}',headers={'access-token':user1_access_token})
    assert resp.status_code==403

#상품 삭제 테스트
def test_delete_product(client):
    #샘플 상품들 등록
    sample_data_len=5
    data={
            "category": "음료",
            "net_price": 3000,
            "cost_price": 2000,
            "name": "우유라떼",
            "description": "고소하고 맛있습니다.",
            "barcode": "1234567891234",
            "expiration_date": "2023-05-20",
            "size": "small"
        }
    page=1
    data_list=[]
    for i in range(sample_data_len):
        sample_data=copy.deepcopy(data)
        sample_data["net_price"]=i*1000
        data_list.append(sample_data)
    
    for sample_data in data_list:
        resp=client.post('/products',json=(sample_data),headers={'access-token':User2.access_token})
        assert resp.status_code==Created_201.status_code


    #상품삭제 후 자신의 상품 조회
    resp=client.delete(f'/products/{Product1.product_id}',headers={'access-token':User2.access_token})
    assert resp.status_code==Get_200.status_code

    resp=client.get(f'/products/{Product1.product_id}',headers={'access-token':User2.access_token})
    assert resp.status_code==403

    #상품 삭제 후 자신의 상품 리스트 조회
    page=1
    resp=client.get(f'/products?page={page}',headers={'access-token':User2.access_token})
    assert resp.status_code==Get_200.status_code
    
    resp_data=get_data(resp.json())
    assert len(resp_data["products"])==sample_data_len

#상품검색 테스트 (업데이트 후 검색도)
def test_get_search_product(client):
    #상품 등록 및 검색
    data_list=[{
            "category": "음료",
            "net_price": 3000,
            "cost_price": 2000,
            "name": "아이스 라떼",
            "description": "고소하고 맛있습니다.",
            "barcode": "1234567891234",
            "expiration_date": "2023-05-20",
            "size": "small"
        },
        {
            "category": "과자",
            "net_price": 3000,
            "cost_price": 2000,
            "name": "땅콩 꽈배기",
            "description": "고소하고 맛있습니다.",
            "barcode": "1234567891234",
            "expiration_date": "2023-05-20",
            "size": "small"
        },
        {
            "category": "주류",
            "net_price": 3000,
            "cost_price": 2000,
            "name": "시원Soju",
            "description": "고소하고 맛있습니다.",
            "barcode": "1234567891234",
            "expiration_date": "2023-05-20",
            "size": "small"
        }]
    for sample_data in data_list:
        resp=client.post('/products',json=(sample_data),headers={'access-token':User2.access_token})
        assert resp.status_code==Created_201.status_code

    #초성검색
    resp=client.get(f'/search/products?name=ㄸㅋ',headers={'access-token':User2.access_token})
    resp_data=get_data(resp.json())
    assert len(resp_data["products"])==1
    product=resp_data["products"][0]
    assert product["name"]=="땅콩 꽈배기"
    
    nut_product_id=product["id"]
    
    resp=client.get(f'/search/products?name=ㄸㅋ ㄲㅂㄱ',headers={'access-token':User2.access_token})
    resp_data=get_data(resp.json())
    assert len(resp_data["products"])==1
    product=resp_data["products"][0]
    assert product["name"]=="땅콩 꽈배기"
    
    #단어검색
    resp=client.get(f'/search/products?name=아이스',headers={'access-token':User2.access_token})
    resp_data=get_data(resp.json())
    assert len(resp_data["products"])==1
    product=resp_data["products"][0]
    assert product["name"]=="아이스 라떼"
    
    #영어검색
    resp=client.get(f'/search/products?name=So',headers={'access-token':User2.access_token})
    resp_data=get_data(resp.json())
    assert len(resp_data["products"])==1
    product=resp_data["products"][0]
    assert product["name"]=="시원Soju"

    #없는 것 검색
    resp=client.get(f'/search/products?name=꽈기',headers={'access-token':User2.access_token})
    resp_data=get_data(resp.json())
    assert len(resp_data["products"])==0

    #꽈배기 상품 업데이트 후 재검색
    update_name_data={
        "name":"달콤 바삭 꽈배기"
    }
    resp=client.put(f'/products/{nut_product_id}',json=(update_name_data),headers={'access-token':User2.access_token})
    assert resp.status_code==Created_201.status_code
    resp=client.get(f'/search/products?name=달콤',headers={'access-token':User2.access_token})
    resp_data=get_data(resp.json())
    assert len(resp_data["products"])==1
    product=resp_data["products"][0]
    assert product["name"]=="달콤 바삭 꽈배기"
    
    resp=client.get(f'/search/products?name=ㄷㅋ ㅂㅅ',headers={'access-token':User2.access_token})
    resp_data=get_data(resp.json())
    assert len(resp_data["products"])==1
    product=resp_data["products"][0]
    assert product["name"]=="달콤 바삭 꽈배기"
    
    #꽤배기 상품 삭제 후 검색
    resp=client.delete(f'/products/{nut_product_id}',headers={'access-token':User2.access_token})
    assert resp.status_code==Get_200.status_code

    resp=client.get(f'/search/products?name=ㄷㅋ ㅂㅅ',headers={'access-token':User2.access_token})
    resp_data=get_data(resp.json())
    assert len(resp_data["products"])==0


    
    
    


    

    


    

