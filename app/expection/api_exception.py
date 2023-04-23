class PhoneNumberExists(Exception):
    status_code=401
    def __str__(self):
        return "The Phone number is already exists"

class UserWasDeleted(Exception):
    status_code=402
    def __str__(self):
        return "The user with phone bumber was deleted"

