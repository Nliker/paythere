import os,sys

sys.path.append((os.path.dirname(os.path.abspath(os.path.dirname(__file__)))))

from exception import DatabaseError
from schema import *

class ProductService:
    def __init__(self,product_model,conf):
        self.conf=conf
        self.product_model=product_model
    
    def set_db(self,db):
        self.product_model.set_db(db)
        return self

    def create_new_product(self,new_product: CreateProduct,user_id: int)->int:
        """
            새로운 상품을 생성합니다.
        """
        try:
            inserted_product=self.product_model.insert_product(InsertProduct(**new_product.dict(),user_id=user_id))
            
            return inserted_product.id
        except DatabaseError as es:
            raise es
    
    def get_product_info_by_id(self,product_id: int)->ProductInfo:
        """
            상품의 번호를 통해 상품의 정보를 불러옵니다.
        """
        try:
            product=self.product_model.select_product_by_id(product_id)
            product_info=ProductInfo(**product.dict())
            return product_info
        except DatabaseError as es:
            raise es
        