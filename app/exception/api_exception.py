class PhoneNumberExists(Exception):
    status_code=401
    def __str__(self):
        return "The Phone number is already exists"

class UserWasDeleted(Exception):
    status_code=401
    def __str__(self):
        return "The user was deleted"

class PhoneNumberNotExists(Exception):
    status_code=401
    def __str__(self):
        return "The User with phone number is not exists"

class PasswordNotAuthorized(Exception):
    status_code=401
    def __str__(self):
        return "The password was not authorized"
    
class UserIdNotExists(Exception):
    status_code=401
    def __str__(self):
        return "The user is not exists"
    
class ProductIdNotExists(Exception):
    status_code=404
    def __str__(self):
        return "The product is not exists"
    
class ProductWasDeleted(Exception):
    status_code=403
    def __str__(self):
        return "The product was deleted"

class ProductUpdatFailed(Exception):
    status_code=202
    def __str__(self):
        return "Product update was failed"
    
class ProductNotAuthorizedByUser(Exception):
    status_code=403
    def __str__(self):
        return "User has no rights with Product"

class BrokenToken(Exception):
    status_code=401
    def __str__(self):
        return "The access_token was broken"
    
class WrongToken(Exception):
    status_code=401
    def __str__(self):
        return "The access_token payload is not authorized"

class TokenNotExists(Exception):
    status_code=401
    def __str__(self):
        return "The access_token is not exists"
    

