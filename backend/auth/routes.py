from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from passlib.context import CryptContext

from core.database import SessionLocal
from auth.models import User
from auth.schemas import UserCreate, UserResponse

router = APIRouter(prefix="/users", tags=["Users"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_db():
    db = SessionLocal()

    try:
        yield db 
    finally:
        db.close()

def hash_password(password: str) -> str:
    return pwd_context.hash(password)


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    try:
        db_user = User(
            email=user.email,
            hashed_password=hash_password(user.password),
            full_name=user.full_name,
            role=user.role,
            organization=user.organization
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with this email already exists"
        )
    
    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create user"
        )