import sys,os
from fastapi import Depends,APIRouter,Response
from sql import get_db
from sqlalchemy.orm import Session
from schema import *
from auth import verify_token
import traceback
import exception
from response import *

product_api=APIRouter(prefix="/products",tags=["products"])

def product_router(app,services):
    user_service=services.user_service
    product_service=services.product_service

    app.include_router(product_api)

    @product_api.post("/",status_code=Created_201.status_code,response_model=PostProductResponse)
    async def post_product(response: Response,new_product:CreateProduct,current_user_id: int = Depends(verify_token),db: Session = Depends(get_db)):
        """
            상품을 생성합니다.
        """
        try:
            user_existance=user_service.set_db(db).is_user_id_exists(current_user_id)
            if user_existance==False:
                raise exception.UserIdNotExists()

            user_deleted=user_service.set_db(db).is_user_deleted_by_id(current_user_id)
            if user_deleted==True:
                raise exception.UserWasDeleted()
            
            created_product_id=product_service.set_db(db).create_new_product(new_product,current_user_id)
            created_product_info=product_service.set_db(db).get_product_info_by_id(created_product_id)
            
            return make_http_response_json(Created_201,{"product":created_product_info})
        except Exception as es:
                if exception.exceptions_dict.get(es.__class__.__name__,False):
                    response.status_code=es.status_code
                    return exception.make_http_error(es.status_code,es.__str__())
                else:
                    print(traceback.format_exc())
                    response.status_code=500
                    return exception.make_http_error(500,es.__str__())

    @product_api.put("/{product_id}",status_code=Created_201.status_code,response_model=PutProductResponse)
    async def put_product(response: Response,update_product:UpdateProduct,current_user_id: int = Depends(verify_token),db: Session = Depends(get_db)):
        """
            상품의 정보를 업데이트 합니다.
        """
        try:
            return make_http_response_json(Created_201,{"product":"good"})
        except Exception as es:
                if exception.exceptions_dict.get(es.__class__.__name__,False):
                    response.status_code=es.status_code
                    return exception.make_http_error(es.status_code,es.__str__())
                else:
                    print(traceback.format_exc())
                    response.status_code=500
                    return exception.make_http_error(500,es.__str__())
    
    @product_api.get("/{product_id}",status_code=Get_200.status_code,response_model=GetProductResponse)
    async def get_product(response: Response,product_id: int,current_user_id: int = Depends(verify_token),db: Session = Depends(get_db)):
        """
            상품을 조회합니다.
        """
        try:
            return make_http_response_json(Get_200,{"product":"good"})
        except Exception as es:
                if exception.exceptions_dict.get(es.__class__.__name__,False):
                    response.status_code=es.status_code
                    return exception.make_http_error(es.status_code,es.__str__())
                else:
                    print(traceback.format_exc())
                    response.status_code=500
                    return exception.make_http_error(500,es.__str__())
    
    @product_api.get("/",status_code=Get_200.status_code,response_model=GetProductsResponse)
    async def get_products(response: Response,current_user_id: int = Depends(verify_token),db: Session = Depends(get_db)):
        """
            상품들을 조회합니다.
        """
        try:
            return make_http_response_json(Get_200,{"product":"good"})
        except Exception as es:
                if exception.exceptions_dict.get(es.__class__.__name__,False):
                    response.status_code=es.status_code
                    return exception.make_http_error(es.status_code,es.__str__())
                else:
                    print(traceback.format_exc())
                    response.status_code=500
                    return exception.make_http_error(500,es.__str__())
                
    @product_api.delete("/{product_id}",status_code=Get_200.status_code,response_model=DeleteProductResponse)
    async def delete_product(response: Response,product_id: int,current_user_id: int = Depends(verify_token),db: Session = Depends(get_db)):
        """
            상품을 삭제합니다.
        """
        try:
            return make_http_response_json(Get_200,{"product":"good"})
        except Exception as es:
                if exception.exceptions_dict.get(es.__class__.__name__,False):
                    response.status_code=es.status_code
                    return exception.make_http_error(es.status_code,es.__str__())
                else:
                    print(traceback.format_exc())
                    response.status_code=500
                    return exception.make_http_error(500,es.__str__())