class Error(Exception):
    pass

class ItemIdNotFoundError(Error):
    pass

class ListNameNotFoundError(Error):
    pass

class ListNameConflictError(Error):
    pass