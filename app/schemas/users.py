from pydantic import BaseModel


class UserBase(BaseModel):
    username: str


class UserRegister(UserBase):
    name: str
    email: str
    password: str
    password_confirm: str


class UserLogin(UserBase):
    password: str
