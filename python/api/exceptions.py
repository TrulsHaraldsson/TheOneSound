class BadRequest(Exception):
    """
    This is issued when an api-query have bad syntax
    """
    def __init__(self, message):
        super(BadRequest, self).__init__(message)


class EntityNotFound(Exception):
    """
    This is issued when an entity is queried using an ID
    but is not found.
    """
    def __init__(self, message):
        super(EntityNotFound, self).__init__(message)