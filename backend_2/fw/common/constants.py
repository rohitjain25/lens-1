import inspect
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

class WaitTime(Constants):
    ACCESS_TOKEN_EXPIRE_MINUTES = 60
    
    # def keys():
    #     """Return a list of the constants defined by this class."""
    #     attributes = []
    #     for attribute in WaitTime.__dict__.keys():
    #         if not(attribute.startswith('__') and attribute.endswith('__')):
    #             attributes.append(attribute)
    #     return attributes


class Authorization_Level(Constants):
    LEVEL_1 = "level_1"
    LEVEL_2 = "level_2"
    LEVEL_3 = "level_3"
    LEVEL_4 = "level_4"
    LEVEL_5 = "level_5"
