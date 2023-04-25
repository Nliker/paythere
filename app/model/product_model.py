import os,sys
import sql
from exception import DatabaseError
sys.path.append((os.path.dirname(os.path.abspath(os.path.dirname(__file__)))))
import traceback
from schema import *
from typing import List

class ProductModel:
    def set_db(self,db):
        self.db=db

    def insert_product(self,new_product: InsertProduct)->int:
        """
            새로운 상품의 정보를 삽입합니다.
        """
        try:
            new_product=sql.Product(
                **new_product.dict()
            )
            self.db.add(new_product)
        except:
            self.db.rollback()
            raise DatabaseError()
        else:
            self.db.commit()
            self.db.refresh(new_product)
            new_product=Product(**new_product.__dict__)
            return new_product
        
    def select_product_by_id(self,product_id: int)->Product:
        """
            상품의 번호와 일치하는 상품을 조회합니다.
        """
        try:
            product=self.db.query(sql.Product).filter(sql.Product.id==product_id).first()
        except:
            raise DatabaseError()
        else:
            if product!=None:
                product=Product(**product.__dict__)
            return product
        
    def update_product_by_id(self,fitered_update_product: dict,product_id: int)->int:
        """
            상품의 번호와 일치하는 상품의 정보를 업데이트 합니다.
        """
        try:
            result=self.db.query(sql.Product).filter(sql.Product.id==product_id).update(fitered_update_product)
        except:
            raise DatabaseError()
        else:
            self.db.commit()
            return result

    def select_product_by_user_id_with_page(self,user_id: int,page: int)->List[Product]:
        """
            page당 10개의 유저의 상품들을 조회합니다.
        """
        try:
            product_list=self.db.query(sql.Product).filter(sql.Product.user_id==user_id).order_by(sql.Product.created_at.asc()).limit(page*10).all()
        except:
            raise DatabaseError()
        else:
            product_list=[Product(**product.__dict__) for product in product_list]
            return product_list
        

    def select_product_by_user_id_with_name(self,name: str,user_id: int)->List[Product]:
        """
            상풍의 이름이 포함된 상품들을 조회합니다.
        """
        try:
            like_query=f"%{name}%"
            product_list=self.db.query(sql.Product).filter(sql.Product.user_id==user_id,sql.Product.name.like(like_query)).all()
        except:
            raise DatabaseError()
        else:
            product_list=[Product(**product.__dict__) for product in product_list]
            return product_list
    
    def select_product_by_user_id_with_name(self,initial: str,user_id: int)->List[Product]:
        """
            상풍의 
        """
        try:
            like_query=f"%{initial}%"
            product_list=self.db.query(sql.ProductInitial).filter(sql.ProductInitial.initial.like(like_query)).join(sql.Product.id).filter(sql.Product.id==user_id).all()
        except:
            raise DatabaseError()
        else:
            product_list=[Product(**product.__dict__) for product in product_list]
            return product_list