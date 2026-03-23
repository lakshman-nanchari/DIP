import uuid

from fastapi import APIRouter, UploadFile, File, Form, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import select

from core.database import SessionLocal
from core.dependencies import get_current_user
from core.supabase_client import supabase

from auth.models import User
from datasets.models import Dataset
from datasets.schemas import DatasetResponse
from datasets.services import load_dataset, dataset_summary, dataset_preview


router = APIRouter(prefix="/datasets", tags=["Datasets"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


#  UPLOAD DATASET (FIXED)
@router.post("/upload", response_model=DatasetResponse)
async def upload_dataset(
    file: UploadFile = File(...),
    dataset_name: str | None = Form(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    filename = dataset_name if dataset_name else file.filename
    uploaded_filename = file.filename.lower()

    if not uploaded_filename.endswith((".csv", ".xlsx", ".xls")):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only CSV or Excel files are allowed"
        )

    try:
        #  Read file
        file_bytes = await file.read()

        #  File size validation (10MB)
        if len(file_bytes) > 10 * 1024 * 1024:
            raise HTTPException(
                status_code=400,
                detail="File too large (max 10MB)"
            )

        # Unique name
        unique_name = f"{uuid.uuid4()}_{file.filename}"

        #  Upload to Supabase
        response = supabase.storage.from_("datasets").upload(
            unique_name,
            file_bytes
        )

        #  Check upload success
        if isinstance(response, dict) and response.get("error"):
            raise RuntimeError(response["error"])

        # Get public URL
        file_url = supabase.storage.from_("datasets").get_public_url(unique_name)

        # Load dataset
        df = load_dataset(file_url)
        summary = dataset_summary(df)

        dataset = Dataset(
            name=filename,
            file_path=file_url,
            file_type=uploaded_filename.split(".")[-1],
            uploaded_by=current_user.id,
            rows=summary["rows"],
            columns=summary["columns"]
        )

        db.add(dataset)
        db.commit()
        db.refresh(dataset)

        return dataset

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Upload failed: {str(e)}"
        )


#  PREVIEW DATASET
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
        return dataset_preview(df)

    except RuntimeError:
        raise HTTPException(
            status_code=500,
            detail="Failed to generate dataset preview"
        )


#  LIST DATASETS
@router.get("/", response_model=list[DatasetResponse])
def list_datasets(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return db.query(Dataset).filter(
        Dataset.uploaded_by == current_user.id
    ).all()


#  GET SINGLE DATASET
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


#  DELETE DATASET
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
        file_name = dataset.file_path.split("/")[-1]

        supabase.storage.from_("datasets").remove([file_name])

        db.delete(dataset)
        db.commit()

        return {"message": "Dataset deleted successfully"}

    except Exception:
        db.rollback()

        raise HTTPException(
            status_code=500,
            detail="Failed to delete dataset"
        )