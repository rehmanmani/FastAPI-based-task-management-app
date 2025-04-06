# Authentication logic for password hashing and JWT handling
from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import jwt, JWTError
from fastapi import HTTPException

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT configuration
SECRET_KEY = "mysecretkey"  # Replace with a secure key in production
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_jwt_token(user_id: int) -> str:
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = {"sub": str(user_id), "exp": expire}
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def get_user_from_token(token: str) -> int:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return int(payload["sub"])
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")