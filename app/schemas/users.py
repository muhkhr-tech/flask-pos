from pydantic import BaseModel


class UserBase(BaseModel):
    username: str


class UserRegister(UserBase):
    name: str
    email: str
    password: str
    password_confirm: str


class CashierCreate(UserBase):
    password: str
    confirmed_password: str
    role: str = "cashier"


class UserLogin(UserBase):
    password: str
