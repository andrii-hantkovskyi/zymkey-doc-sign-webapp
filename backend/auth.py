import time

from db import create_user as db_create_user
from db import get_user as db_get_user
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from models import Token, User, UserCreate, UserInDB
from passlib.context import CryptContext
from settings import ACCESS_TOKEN_EXPIRE_SECONDS, ALGORITHM, SECRET_KEY

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def create_access_token(data: dict):
    to_encode = data.copy()
    to_encode["exp"] = int(time.time()) + ACCESS_TOKEN_EXPIRE_SECONDS
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


async def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise credentials_exception
        user_data = await db_get_user(username)
        if user_data is None:
            raise credentials_exception
        return UserInDB(**user_data)
    except JWTError:
        raise credentials_exception


async def admin_required(user: User = Depends(get_current_user)):
    if not user.is_admin:
        raise HTTPException(status_code=403, detail="Admins only")
    return user


@router.post("/token", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user_data = await db_get_user(form_data.username)
    if not user_data or not verify_password(
        form_data.password, user_data["hashed_password"]
    ):
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    token = create_access_token(data={"sub": user_data["username"], "is_admin": user_data["is_admin"]})
    return {"access_token": token}


@router.post("/register")
async def register(data: UserCreate):
    existing_user = await db_get_user(data.username)
    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")
    hashed_password = get_password_hash(data.password)
    await db_create_user(data.username, hashed_password, is_admin=False)
    return {"msg": "User registered successfully"}
