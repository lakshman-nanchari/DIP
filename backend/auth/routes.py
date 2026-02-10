from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from passlib.context import CryptContext
from sqlalchemy import select 

from core.database import SessionLocal
from core.security import verify_password, create_access_token
from auth.models import User
from auth.schemas import UserCreate, UserResponse, LoginRequest, TokenResponse


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
    

@router.post("/login", response_model=TokenResponse)
def login(user: LoginRequest, db: Session = Depends(get_db)):
    db_user = db.execute(
        select(User).where(User.email == user.email)   
    ).scalar_one_or_none()

    #do not reveal which field is wrong 
    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    if not db_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is inactive"
        )
    
    try:
        access_token = create_access_token(
            data={
                "sub": str(db_user.id),
                "role": db_user.role
            }
        )
    except RuntimeError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to generate access token"
        )
    
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }