from pydantic import BaseModel, StrictStr

from fw.common.constants import Authorization_Level


class LoginForm(BaseModel):
    email: StrictStr
    password: StrictStr


class SignupForm(BaseModel):
    email: StrictStr
    password: StrictStr
    first_name: StrictStr
    last_name: StrictStr
    role:StrictStr = None

class DeleteForm(BaseModel):
    email:StrictStr
    
class SignupResponseModel(BaseModel):
    email: StrictStr
    first_name: StrictStr
    last_name: StrictStr
    role:StrictStr = None