from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import JWTError, jwt
from config import TOKEN_EXPIRE_MINUTES, ALGORITHM, SECRET_KEY


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_timedelta: timedelta = None) -> str:
    to_encode = data.copy()
    if not expires_timedelta:
        expires_timedelta = timedelta(minutes=TOKEN_EXPIRE_MINUTES)
    expire = datetime.utcnow() + expires_timedelta
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
