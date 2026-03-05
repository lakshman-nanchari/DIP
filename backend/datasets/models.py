from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from core.database import Base


class Dataset(Base):
    __tablename__ = "datasets"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String(255), nullable=False)

    file_path = Column(String(500), nullable=False)

    file_type = Column(String(50))

    uploaded_by = Column(Integer, ForeignKey("users.id"))

    rows = Column(Integer)
    columns = Column(Integer)

    created_at = Column(DateTime(timezone=True), server_default=func.now())