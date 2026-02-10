from datetime import datetime, timedelta
from jose import jwt, JWTError, ExpiredSignatureError
from passlib.context import CryptContext

from core.config import SECRET_KEY

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    try:
        return pwd_context.verify(plain_password, hashed_password)
    except Exception:
        return False
    
def create_access_token(data: dict, exprires_delta: timedelta | None = None) -> str :
    if not SECRET_KEY:
        raise RuntimeError("SECRET_KEY is not configured")
    try:
        to_encode = data.copy()
        expire = datetime.utcnow() + (
            exprires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
            )
        to_encode.update({"exp": expire})

        return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    except Exception as e:
        raise RuntimeError("Failed to create access token") from e
    

def decode_access_token(token: str) -> dict:
    if not SECRET_KEY:
        raise RuntimeError("SECRET_KEY is not configured")
    
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    
    except ExpiredSignatureError:
        raise ValueError("Token has expired")
    
    except JWTError:
        raise ValueError("Invalid token")