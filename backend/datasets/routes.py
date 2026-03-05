import os
from fastapi import APIRouter, UploadFile, File, Depends, HTTPException, status
from sqlalchemy.orm import Session

from core.database import SessionLocal
from core.dependencies import get_current_user
from auth.models import User

from datasets.models import Dataset
from datasets.schemas import DatasetResponse
from datasets.services import load_dataset, dataset_summary


router = APIRouter(prefix="/datasets", tags=["Datasets"])


UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/upload", response_model=DatasetResponse)
async def upload_dataset(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    filename = file.filename

    if not filename.endswith((".csv", ".xlsx", ".xls")):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only CSV or Excel files are allowed"
        )

    file_path = os.path.join(UPLOAD_DIR, filename)

    try:
        with open(file_path, "wb") as buffer:
            buffer.write(await file.read())

        df = load_dataset(file_path)

        summary = dataset_summary(df)

        dataset = Dataset(
            name=filename,
            file_path=file_path,
            file_type=filename.split(".")[-1],
            uploaded_by=current_user.id,
            rows=summary["rows"],
            columns=summary["columns"]
        )

        db.add(dataset)
        db.commit()
        db.refresh(dataset)

        return dataset

    except RuntimeError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Dataset processing failed"
        )