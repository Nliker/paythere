class PhoneNumberExists(Exception):
    status_code=401
    def __str__(self):
        return "The Phone number is already exists"

class UserWasDeleted(Exception):
    status_code=401
    def __str__(self):
        return "The user with phone number was deleted"

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
        return "The user_id is not exists"