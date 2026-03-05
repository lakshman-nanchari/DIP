from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select

from core.database import SessionLocal
from core.dependencies import get_current_user

from datasets.models import Dataset
from datasets.services import load_dataset

from analytics.services import generate_profile, generate_insights


router = APIRouter(prefix="/analytics", tags=["Analytics"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/{dataset_id}/profile")
def dataset_profile(
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

        profile = generate_profile(df)

        return profile

    except RuntimeError:
        raise HTTPException(
            status_code=500,
            detail="Failed to analyze dataset"
        )
    

@router.get("/{dataset_id}/insights")
def dataset_insights(
    dataset_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):

    dataset = db.execute(
        select(Dataset).where(Dataset.id == dataset_id)
    ).scalar_one_or_none()

    if not dataset:
        raise HTTPException(status_code=404, detail="Dataset not found")

    try:
        df = load_dataset(dataset.file_path)

        insights = generate_insights(df)

        return {
            "dataset_id": dataset_id,
            "insights": insights
        }

    except RuntimeError:
        raise HTTPException(
            status_code=500,
            detail="Failed to generate insights"
        )