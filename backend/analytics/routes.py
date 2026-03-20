from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select
import math

from core.database import SessionLocal
from core.dependencies import get_current_user

from datasets.models import Dataset
from datasets.services import load_dataset

from analytics.services import (
    generate_profile,
    generate_insights,
    generate_business_insights,
    generate_forecast,
    clean_dataset,
    generate_charts,
    generate_kpis,
    generate_dashboard,
    detect_anomalies,
    cached_dashboard,
    get_df_hash
)

router = APIRouter(prefix="/analytics", tags=["Analytics"])


# DB DEPENDENCY

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# HELPER 

def get_user_dataset(dataset_id, db, user_id):
    dataset = db.execute(
        select(Dataset).where(
            Dataset.id == dataset_id,
            Dataset.uploaded_by == user_id
        )
    ).scalar_one_or_none()

    if not dataset:
        raise HTTPException(status_code=404, detail="Dataset not found")

    return dataset


# PROFILE

@router.get("/{dataset_id}/profile")
def dataset_profile(
    dataset_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    dataset = get_user_dataset(dataset_id, db, current_user.id)

    try:
        df = load_dataset(dataset.file_path)
        return generate_profile(df)

    except Exception:
        raise HTTPException(500, "Failed to analyze dataset")


# INSIGHTS

@router.get("/{dataset_id}/insights")
def dataset_insights(
    dataset_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    dataset = get_user_dataset(dataset_id, db, current_user.id)

    try:
        df = load_dataset(dataset.file_path)

        statistical = generate_insights(df)
        business = generate_business_insights(df)

        return {
            "dataset_id": dataset_id,
            "summary": statistical.get("summary", {}),
            "statistical_insights": statistical.get("insights", []),
            "business_insights": business
        }

    except Exception as e:
        raise HTTPException(500, f"Insights failed: {str(e)}")

# FORECAST

@router.get("/{dataset_id}/forecast")
def dataset_forecast(
    dataset_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    dataset = get_user_dataset(dataset_id, db, current_user.id)

    try:
        df = load_dataset(dataset.file_path)

        return {
            "dataset_id": dataset_id,
            "forecast": generate_forecast(df)
        }

    except RuntimeError as e:
        raise HTTPException(400, str(e))


# CLEAN DATASET

@router.post("/{dataset_id}/clean")
def clean_dataset_api(
    dataset_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    dataset = get_user_dataset(dataset_id, db, current_user.id)

    try:
        df = load_dataset(dataset.file_path)
        cleaned_df, report = clean_dataset(df)

        if dataset.file_type == "csv":
            cleaned_df.to_csv(dataset.file_path, index=False)
        else:
            cleaned_df.to_excel(dataset.file_path, index=False)

        return {
            "dataset_id": dataset_id,
            "cleaning_report": report
        }

    except Exception as e:
        raise HTTPException(500, str(e))


# CHARTS

@router.get("/{dataset_id}/charts")
def dataset_charts(
    dataset_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    dataset = get_user_dataset(dataset_id, db, current_user.id)

    try:
        df = load_dataset(dataset.file_path)

        charts = generate_charts(df)

        chart_count = sum(
            len(v) if isinstance(v, dict) else 1
            for v in charts.values()
        )

        return {
            "dataset_id": dataset_id,
            "chart_count": chart_count,
            "charts": charts
        }

    except Exception as e:
        raise HTTPException(500, f"Chart generation failed: {str(e)}")


# KPIs

@router.get("/{dataset_id}/kpis")
def dataset_kpis(
    dataset_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    dataset = get_user_dataset(dataset_id, db, current_user.id)

    try:
        df = load_dataset(dataset.file_path)

        return {
            "dataset_id": dataset_id,
            "kpis": generate_kpis(df)
        }

    except RuntimeError as e:
        raise HTTPException(400, str(e))

    except Exception as e:
        raise HTTPException(500, f"KPI failed: {str(e)}")


# ANOMALIES

@router.get("/{dataset_id}/anomalies")
def dataset_anomalies(
    dataset_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    dataset = get_user_dataset(dataset_id, db, current_user.id)

    try:
        df = load_dataset(dataset.file_path)

        return {
            "dataset_id": dataset_id,
            "anomaly_analysis": detect_anomalies(df)
        }

    except RuntimeError as e:
        raise HTTPException(400, str(e))

    except Exception:
        raise HTTPException(500, "Anomaly detection failed")


# DASHBOARD (CACHED)

@router.get("/{dataset_id}/dashboard")
def dataset_dashboard(
    dataset_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    dataset = get_user_dataset(dataset_id, db, current_user.id)

    try:
        df = load_dataset(dataset.file_path)

        #  CACHING
        df_hash = get_df_hash(df)
        df_json = df.to_json()

        dashboard = cached_dashboard(df_hash, df_json)

        # Clean NaN
        def clean_nan(obj):
            if isinstance(obj, dict):
                return {k: clean_nan(v) for k, v in obj.items()}
            elif isinstance(obj, list):
                return [clean_nan(v) for v in obj]
            elif isinstance(obj, float) and math.isnan(obj):
                return None
            return obj

        dashboard = clean_nan(dashboard)

        return {
            "dataset_id": dataset_id,
            "dataset_name": dataset.name,
            "dashboard": dashboard
        }

    except RuntimeError as e:
        raise HTTPException(400, str(e))

    except Exception:
        raise HTTPException(500, "Dashboard generation failed")