from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select

from core.database import SessionLocal
from core.dependencies import get_current_user

from datasets.models import Dataset
from datasets.services import load_dataset

from analytics.services import generate_profile, generate_insights, generate_forecast, clean_dataset
from analytics.services import generate_charts, generate_insights, generate_kpis, generate_dashboard, detect_anomalies

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
    

@router.get("/{dataset_id}/forecast")
def dataset_forecast(
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

        forecast = generate_forecast(df) 
        return {
            "dataset_id": dataset_id,
            "forecast": forecast
        } 
    
    except RuntimeError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        ) 
    

@router.post("/{dataset_id}/clean")
def clean_dataset_api(
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

        cleaned_df, report = clean_dataset(df)

        cleaned_df.to_csv(dataset.file_path, index=False)

        return {
            "dataset_id": dataset_id,
            "cleaning_report": report
        }

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Failed to clean dataset"
        ) 
    


@router.get("/{dataset_id}/charts")
def dataset_charts(
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

        charts = generate_charts(df)

        return {
            "dataset_id": dataset_id,
            "charts": charts
        }

    except RuntimeError:
        raise HTTPException(
            status_code=500,
            detail="Failed to generate chart data"
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
            "analysis": insights
        }

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Failed to generate insights"
        ) 
    
@router.get("/{dataset_id}/kpis")
def dataset_kpis(
    dataset_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):

    dataset = db.execute(
        select(Dataset).where(Dataset.id == dataset_id)
    ).scalar_one_or_none()

    if not dataset:
        raise HTTPException(
            status_code=404,
            detail="Dataset not found"
        )

    try:
        df = load_dataset(dataset.file_path)

        kpis = generate_kpis(df)

        return {
            "dataset_id": dataset_id,
            "kpis": kpis
        }

    except RuntimeError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Failed to generate KPIs"
        ) 
    
@router.get("/{dataset_id}/dashboard") 
def dataset_dashboard( 
    dataset_id: int, 
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    dataset = db.execute( 
        select(Dataset).where(Dataset.id == dataset_id)
    ).scalar_one_or_none() 

    if not dataset:
        raise HTTPException(
            status_code=404, 
            detail="Dataset not found"
        ) 
    try: 
        df = load_dataset(dataset.file_path) 

        dashboard = generate_dashboard(df) 

        return {
            "dataset_id": dataset_id,
            "dashboard": dashboard
        }

    except RuntimeError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Failed to generate dashboard"
        ) 
    

@router.get("/{dataset_id}/anomalies")
def dataset_anomalies(
    dataset_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):

    dataset = db.execute(
        select(Dataset).where(Dataset.id == dataset_id)
    ).scalar_one_or_none()

    if not dataset:
        raise HTTPException(
            status_code=404,
            detail="Dataset not found"
        )

    try:

        df = load_dataset(dataset.file_path)

        anomalies = detect_anomalies(df)

        return {
            "dataset_id": dataset_id,
            "anomaly_analysis": anomalies
        }

    except RuntimeError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Failed to detect anomalies"
        )