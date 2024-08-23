from enum import Enum, IntEnum

class Quality(Enum):
    SOURCE = {'name': 'Source', 'value': 'chuncked', 'resolution': 'source', 'fps': 0.00}

class HTTPStatusCode(IntEnum):
    OK = 200
    BAD_REQUEST = 400
    UNAUTHORIZED = 401
    FORBIDDEN = 403
    NOT_FOUND = 404
    SERVER_ERROR = 500