from pydantic import BaseModel


class User(BaseModel):
    username: str
    is_admin: bool


class UserInDB(User):
    hashed_password: str


class Token(BaseModel):
    access_token: str


class UserCreate(BaseModel):
    username: str
    password: str
