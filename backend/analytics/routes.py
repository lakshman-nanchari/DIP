from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select
import math
import os
import logging

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
    detect_anomalies,
    cached_dashboard,
    get_df_hash
)

#  LOGGING 

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()

logging.basicConfig(level=LOG_LEVEL)
logger = logging.getLogger(__name__)

#  ROUTER 

router = APIRouter(prefix="/analytics", tags=["Analytics"])


# DB 

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


# DATASET CACHE 

def get_dataset_df(
    dataset_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    try:
        dataset = get_user_dataset(dataset_id, db, current_user.id)

        logger.info(f"Loading dataset: {dataset.file_path}")
        df = load_dataset(dataset.file_path)
        logger.info(f"Dataset loaded: {df.shape}")

        return dataset, df

    except Exception as e:
        logger.error(f"Dataset load error: {str(e)}")
        raise HTTPException(500, f"Dataset load error: {str(e)}")


# PROFILE 

@router.get("/{dataset_id}/profile")
def dataset_profile(dataset_data=Depends(get_dataset_df)):
    dataset, df = dataset_data

    try:
        return generate_profile(df)

    except Exception as e:
        logger.error(f"Profile error: {str(e)}")
        raise HTTPException(500, f"Profile error: {str(e)}")


# INSIGHTS 

@router.get("/{dataset_id}/insights")
def dataset_insights(dataset_data=Depends(get_dataset_df)):
    dataset, df = dataset_data

    try:
        statistical = generate_insights(df)
        business = generate_business_insights(df)

        return {
            "dataset_id": dataset.id,
            "summary": statistical.get("summary", {}),
            "statistical_insights": statistical.get("insights", []),
            "business_insights": business
        }

    except Exception as e:
        logger.error(f"Insights error: {str(e)}")
        raise HTTPException(500, f"Insights failed: {str(e)}")


#  FORECAST 

@router.get("/{dataset_id}/forecast")
def dataset_forecast(dataset_data=Depends(get_dataset_df)):
    dataset, df = dataset_data

    try:
        return {
            "dataset_id": dataset.id,
            "forecast": generate_forecast(df)
        }

    except RuntimeError as e:
        logger.warning(f"Forecast error: {str(e)}")
        raise HTTPException(400, str(e))

    except Exception as e:
        logger.error(f"Forecast failure: {str(e)}")
        raise HTTPException(500, f"Forecast error: {str(e)}")


#  CLEAN 

@router.post("/{dataset_id}/clean")
def clean_dataset_api(dataset_data=Depends(get_dataset_df)):
    dataset, df = dataset_data

    try:
        cleaned_df, report = clean_dataset(df)

        if dataset.file_type == "csv":
            cleaned_df.to_csv(dataset.file_path, index=False)
        else:
            cleaned_df.to_excel(dataset.file_path, index=False)

        return {
            "dataset_id": dataset.id,
            "cleaning_report": report
        }

    except Exception as e:
        logger.error(f"Cleaning failed: {str(e)}")
        raise HTTPException(500, str(e))


# CHARTS 

@router.get("/{dataset_id}/charts")
def dataset_charts(dataset_data=Depends(get_dataset_df)):
    dataset, df = dataset_data

    try:
        charts = generate_charts(df)

        chart_count = (
            len(charts.get("histograms", {})) +
            len(charts.get("bars", {})) +
            (1 if charts.get("trend") else 0) +
            (1 if charts.get("correlation_matrix") else 0)
        )

        return {
            "dataset_id": dataset.id,
            "chart_count": chart_count,
            "charts": charts
        }

    except Exception as e:
        logger.error(f"Chart error: {str(e)}")
        raise HTTPException(500, f"Chart generation failed: {str(e)}")


# KPIs 

@router.get("/{dataset_id}/kpis")
def dataset_kpis(dataset_data=Depends(get_dataset_df)):
    dataset, df = dataset_data

    try:
        return {
            "dataset_id": dataset.id,
            "kpis": generate_kpis(df)
        }

    except RuntimeError as e:
        logger.warning(f"KPI error: {str(e)}")
        raise HTTPException(400, str(e))

    except Exception as e:
        logger.error(f"KPI failure: {str(e)}")
        raise HTTPException(500, f"KPI failed: {str(e)}")


#ANOMALIES 

@router.get("/{dataset_id}/anomalies")
def dataset_anomalies(dataset_data=Depends(get_dataset_df)):
    dataset, df = dataset_data

    try:
        return {
            "dataset_id": dataset.id,
            "anomaly_analysis": detect_anomalies(df)
        }

    except RuntimeError as e:
        logger.warning(f"Anomaly error: {str(e)}")
        raise HTTPException(400, str(e))

    except Exception as e:
        logger.error(f"Anomaly failure: {str(e)}")
        raise HTTPException(500, f"Error: {str(e)}")


#  DASHBOARD 

@router.get("/{dataset_id}/dashboard")
def dataset_dashboard(dataset_data=Depends(get_dataset_df)):
    dataset, df = dataset_data

    try:
        dashboard = cached_dashboard(dataset.file_path)

        def clean_nan(obj):
            if isinstance(obj, dict):
                return {k: clean_nan(v) for k, v in obj.items()}
            elif isinstance(obj, list):
                return [clean_nan(v) for v in obj]
            elif isinstance(obj, float) and math.isnan(obj):
                return None
            return obj

        return {
            "dataset_id": dataset.id,
            "dataset_name": dataset.name,
            "dashboard": clean_nan(dashboard)
        }

    except RuntimeError as e:
        logger.warning(f"Dashboard runtime error: {str(e)}")
        raise HTTPException(400, str(e))

    except Exception as e:
        logger.error(f"Dashboard failure: {str(e)}")
        raise HTTPException(500, f"Dashboard error: {str(e)}")