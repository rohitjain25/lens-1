from typing import Annotated, Self
from fastapi import Depends, HTTPException, Response, status
from jose import JWTError, jwt
from datetime import datetime, timedelta
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fw.common.constants import WaitTime
from .model import SignupForm

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def get_current_active_user(token=Depends(oauth2_scheme)):
    print(token)
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token, Authentication.SECRET_KEY, algorithms=[Authentication.ALGORITHM]
        )
        # username: str = payload.get("email", None)
        if payload is None:
            raise credentials_exception

    except JWTError:
        raise credentials_exception
    if payload is None:
        raise credentials_exception
    return payload


class Authentication:
    SECRET_KEY = "0F45E9FCB67D4A73AE19DFA1D8B22E34EB314B12380A17294B801925D68E0489"
    ALGORITHM = "HS256"

    def __init__(self, database):
        self.__database = database
        self.__pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def rbac_custom(self, roles=["level_5"]):
        return _RBAC(roles)

    @property
    def rbac(self):
        return {
            "level_5": self.rbac_custom(
                ["level_5", "level_4", "level_3", "level_2", "level_1"]
            ),
            "level_4": self.rbac_custom(["level_4", "level_3", "level_2", "level_1"]),
            "level_3": self.rbac_custom(["level_3", "level_2", "level_1"]),
            "level_2": self.rbac_custom(["level_2", "level_1"]),
            "level_1": self.rbac_custom(["level_1"]),
        }

    def get_current_user(self, request=Depends(get_current_active_user)):
        print(request)

    def login(self, request, response: Response):
        user = self.__database.authentication.fetch_user(request.email)
        if user is None:
            response.status_code = 401
            return {"error": "Invalid credentials"}
        if self.__verify_password(request.password, user["password"]):
            del user["password"]
            del user["userId"]
            return {"token": self.__create_access_token(user), "token_type": "bearer"}
        else:
            response.status_code = 401
            return {"error": "Invalid credentials"}

    def signup(self, request):
        data = dict(request.__dict__)
        data["password"] = self.__get_password_hash(request.password)
        data["role"] = "level_5"
        self.__database.authentication.signup(data)
        return data

    def __verify_password(self, plain_password, hashed_password):
        return self.__pwd_context.verify(plain_password, hashed_password)

    def __get_password_hash(self, password):
        return self.__pwd_context.hash(password)

    def __create_access_token(
        self,
        data: dict,
        expires_delta: timedelta = timedelta(
            minutes=WaitTime.ACCESS_TOKEN_EXPIRE_MINUTES.value
        ),
    ):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, self.SECRET_KEY, algorithm=self.ALGORITHM)
        return encoded_jwt


class _RBAC:
    """Role Based Access Control"""

    def __init__(self, roles: list[str] = ["level_5"]):
        self.__roles = roles

    def __call__(self, user: dict = Depends(get_current_active_user)):
        user_role = user.get("role", "level_5")
        if user_role not in self.__roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Operation not permitted",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return user
