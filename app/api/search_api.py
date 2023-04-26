from fastapi import Depends,APIRouter,Response
from sql import get_db
from sqlalchemy.orm import Session
from schema import *
from auth import verify_token
import traceback
import exception
from response import *

search_api=APIRouter(prefix="/search",tags=["search"])

def search_router(app,services):
    user_service=services.user_service
    product_service=services.product_service

    app.include_router(search_api)
    
    @search_api.get("/products")
    async def get_search_products(response: Response,name: Optional[str]=None,credentials: dict = Depends(verify_token),db: Session = Depends(get_db)):
        """
            상품의 이름을 검색합니다.
        """
        try:
            current_user_id=credentials["current_user_id"]
            access_token=credentials["access_token"]

            access_token_logouted=user_service.set_db(db).is_user_access_token_logouted(access_token)
            if access_token_logouted==True:
                raise exception.UserLogouted()

            user_existance=user_service.set_db(db).is_user_id_exists(current_user_id)
            if user_existance==False:
                raise exception.UserIdNotExists()

            user_deleted=user_service.set_db(db).is_user_deleted_by_id(current_user_id)
            if user_deleted==True:
                raise exception.UserWasDeleted()

            product_info_list_by_name=product_service.set_db(db).get_user_products_by_name(name,current_user_id)
            return make_http_response_json(Get_200,{"products":product_info_list_by_name})
        except Exception as es:
                if exception.exceptions_dict.get(es.__class__.__name__,False):
                    response.status_code=es.status_code
                    return exception.make_http_error(es.status_code,es.__str__())
                else:
                    print(traceback.format_exc())
                    response.status_code=500
                    return exception.make_http_error(500,es.__str__())