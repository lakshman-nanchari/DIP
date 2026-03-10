from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from core.config import DATABASE_URL

# create engine
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True
)

# session factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# base model
Base = declarative_base()