class ProductService:
    def __init__(self,product_model,conf):
        self.conf=conf
        self.user_model=product_model
    
    def set_db(self,db):
        self.product_model.set_db(db)
    
    def create_user(self,new_product):
        return True