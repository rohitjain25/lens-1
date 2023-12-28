

class MetaConstant(type):
    def __getattr__(cls, key):
        try:
            if key in cls:
                return cls[key]
            else:
                raise Exception(f'Invalid Constant: "{key}" is not in "{cls}"')
        except Exception:
            raise Exception(f'Invalid Constant: "{key}" is not in "{cls}"')

    def __setattr__(cls, key, value):
        raise TypeError


class Constants(object, metaclass=MetaConstant):
    def __getattr__(self, name):
        return self[name]

    def __setattr__(self, name, value):
        raise TypeError


# Classes derived from enums/Constants class
class Status_Code(Constants):
    OK = 200
    CREATED = 201
    ACCEPTED = 202
    NO_CONTENT = 204
    BAD_REQUEST = 400
    UNAUTHORIZED = 401
    FORBIDDEN = 403
    NOT_FOUND = 404
    METHOD_NOT_ALLOWED = 405
    CONFLICT = 409
    GONE = 410
    PRECONDITION_FAILED = 412
    UNPROCESSABLE_ENTITY = 422
    INTERNAL_SERVER_ERROR = 500

class Schema_Files(Constants):
    AUTHENTICATION = "authentication_schema.json"