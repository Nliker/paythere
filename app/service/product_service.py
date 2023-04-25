import os,sys

sys.path.append((os.path.dirname(os.path.abspath(os.path.dirname(__file__)))))
from typing import List
from exception import DatabaseError
from schema import *
from tool import korean_to_initial

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
        
    def is_product_id_exists(self,product_id: int)->bool:
        """
            상품의 번호를 통해 상품의 존재를 확인합니다.
        """
        try:
            product=self.product_model.select_product_by_id(product_id)
            if product!=None:
                return True
            else:
                return False
        except DatabaseError as es:
            raise es

    def is_product_deleted_by_id(self,product_id: int)->bool:
        try:
            product=self.product_model.select_product_by_id(product_id)
            if product!=None and product.deleted==True:
                return True
        except DatabaseError as es:
            raise es

    def update_product_info_by_id(self,update_product: UpdateProduct,product_id: int)->UpdatedProductInfo:
        """
            상품의 번호와 일치하는 상품의 정보를 변경합니다.
        """
        try:
            fitered_update_product=update_product.dict(exclude_unset=True)
            updated_count=self.product_model.update_product_by_id(fitered_update_product,product_id)
            if updated_count==0:
                return False
            else:
                updated_product=self.product_model.select_product_by_id(product_id)
                updated_product_info=UpdatedProductInfo(**updated_product.dict())
            return updated_product_info
        except DatabaseError as es:
            raise es
        
    def is_product_authorized_by_user_id(self,user_id: int,product_id: int)->int:
        """
            상품이 유저의 소유인지를 확인합니다.
        """
        try:
            product=self.product_model.select_product_by_id(product_id)
            if product.user_id==user_id:
                return True
            else:
                return False
        except DatabaseError as es:
            raise es
        
    def get_user_products_by_page(self,user_id: int,page: int)->List[ProductInfo]:
        """
            page당 10개의 유저의 상품 정보를 불러옵니다.(삭제되지 않은 상품만)
        """
        try:
            user_product_list=self.product_model.select_product_by_user_id_with_page(user_id,page)
            user_product_info_list=[ProductInfo(**product.dict()) for product in user_product_list if product.deleted==False]
            return user_product_info_list
        except DatabaseError as es:
            raise es
        
    def delete_product_by_id(self,product_id: int)->int:
        """
            상품 번호와 일치하는 상품을 삭제합니다.
        """
        try:
            result=self.product_model.update_product_by_id({'deleted':True},product_id)
            return result
        except DatabaseError as es:
            raise es
        
    def get_user_products_by_name(self,name: str,user_id: int)->List[ProductInfo]:
        """
            상품의 이름을 통해 검색한 정보들을 불러옵니다.
        """
        try:
            #한글문자열의 초성만을 추출합니다.
            initial_name=korean_to_initial(name)
            
            #추출한 초성과 일치할 경우 초성검색모드로 돌입합니다.
            if initial_name==name:
                user_product_list=self.product_model.select_product_by_user_id_with_name(initial_name,user_id)
            #추출한 초성과 일치하지 않을 경우 일반 검색모드로 돌입합니다.
            else:
                user_product_list=self.product_model.select_product_by_user_id_with_inital(name,user_id)
            
            user_product_info_list=[ProductInfo(**product.dict()) for product in user_product_list if product.deleted==False]
            print(user_product_info_list)
            return user_product_info_list
        except DatabaseError as es:
            raise es