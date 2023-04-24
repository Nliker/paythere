import os,sys
import sql
from exception import DatabaseError
sys.path.append((os.path.dirname(os.path.abspath(os.path.dirname(__file__)))))
import traceback
from schema import *

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