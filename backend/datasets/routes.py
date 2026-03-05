import os
from fastapi import APIRouter, UploadFile, File, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import select
from core.database import SessionLocal
from core.dependencies import get_current_user
from auth.models import User

from datasets.models import Dataset
from datasets.schemas import DatasetResponse
from datasets.services import load_dataset, dataset_summary,dataset_preview


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
    
@router.get("/{dataset_id}/preview")
def preview_dataset(
    dataset_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    dataset = db.execute(
        select(Dataset).where(Dataset.id == dataset_id)
    ).scalar_one_or_none()

    if not dataset:
        raise HTTPException(status_code=404, detail="Dataset not found")
    
    try:
        df = load_dataset(dataset.file_path)
        preview = dataset_preview(df)
        return preview 
    
    except RuntimeError:
        raise HTTPException(
            status_code=500,
            detail="Failed to generate dataset preview"
        ) 
    
@router.get("/", response_model=list[DatasetResponse])
def list_datasets(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    datasets = db.query(Dataset).filter(
        Dataset.uploaded_by == current_user.id
    ).all()

    return datasets 


@router.get("/{dataset_id}", response_model=DatasetResponse)
def get_dataset(
    dataset_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    dataset = db.query(Dataset).filter(
        Dataset.id == dataset_id,
        Dataset.uploaded_by == current_user.id
    ).first()

    if not dataset:
        raise HTTPException(
            status_code=404,
            detail="Dataset not found"
        )

    return dataset  




@router.delete("/{dataset_id}")
def delete_dataset(
    dataset_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    dataset = db.query(Dataset).filter(
        Dataset.id == dataset_id,
        Dataset.uploaded_by == current_user.id
    ).first()

    if not dataset:
        raise HTTPException(
            status_code=404,
            detail="Dataset not found"
        )

    try:

        if os.path.exists(dataset.file_path):
            os.remove(dataset.file_path)

        db.delete(dataset)
        db.commit()

        return {"message": "Dataset deleted successfully"}

    except Exception:
        db.rollback()

        raise HTTPException(
            status_code=500,
            detail="Failed to delete dataset"
        )