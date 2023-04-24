class DatabaseError(Exception):
    status_code=500
    def __str__(self):
        return "Database was not communicated"