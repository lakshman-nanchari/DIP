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
        print("📂 Loading dataset (profile):", dataset.file_path)
        df = load_dataset(dataset.file_path)
        print("✅ Dataset loaded (profile):", df.shape)

        return generate_profile(df)

    except Exception as e:
        print("🔥 PROFILE ERROR:", str(e))
        raise HTTPException(500, f"Profile error: {str(e)}")


# INSIGHTS

@router.get("/{dataset_id}/insights")
def dataset_insights(
    dataset_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    dataset = get_user_dataset(dataset_id, db, current_user.id)

    try:
        print("📂 Loading dataset (insights):", dataset.file_path)
        df = load_dataset(dataset.file_path)
        print("✅ Dataset loaded (insights):", df.shape)

        statistical = generate_insights(df)
        business = generate_business_insights(df)

        return {
            "dataset_id": dataset_id,
            "summary": statistical.get("summary", {}),
            "statistical_insights": statistical.get("insights", []),
            "business_insights": business
        }

    except Exception as e:
        print("🔥 INSIGHTS ERROR:", str(e))
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
        print("📂 Loading dataset (forecast):", dataset.file_path)
        df = load_dataset(dataset.file_path)
        print("✅ Dataset loaded (forecast):", df.shape)

        return {
            "dataset_id": dataset_id,
            "forecast": generate_forecast(df)
        }

    except RuntimeError as e:
        print("⚠️ FORECAST ERROR:", str(e))
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
        print("📂 Loading dataset (clean):", dataset.file_path)
        df = load_dataset(dataset.file_path)
        print("✅ Dataset loaded (clean):", df.shape)

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
        print("🔥 CLEAN ERROR:", str(e))
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
        print("📂 Loading dataset (charts):", dataset.file_path)
        df = load_dataset(dataset.file_path)
        print("✅ Dataset loaded (charts):", df.shape)

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
        print("🔥 CHART ERROR:", str(e))
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
        print("📂 Loading dataset (kpis):", dataset.file_path)
        df = load_dataset(dataset.file_path)
        print("✅ Dataset loaded (kpis):", df.shape)

        return {
            "dataset_id": dataset_id,
            "kpis": generate_kpis(df)
        }

    except RuntimeError as e:
        print("⚠️ KPI ERROR:", str(e))
        raise HTTPException(400, str(e))

    except Exception as e:
        print("🔥 KPI ERROR:", str(e))
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
        print("📂 Loading dataset (anomalies):", dataset.file_path)
        df = load_dataset(dataset.file_path)
        print("✅ Dataset loaded (anomalies):", df.shape)

        return {
            "dataset_id": dataset_id,
            "anomaly_analysis": detect_anomalies(df)
        }

    except RuntimeError as e:
        print("⚠️ ANOMALY ERROR:", str(e))
        raise HTTPException(400, str(e))

    except Exception as e:
        print("🔥 ANOMALY ERROR:", str(e))
        raise HTTPException(500, f"Error: {str(e)}")


# DASHBOARD (CACHED)

@router.get("/{dataset_id}/dashboard")
def dataset_dashboard(
    dataset_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    dataset = get_user_dataset(dataset_id, db, current_user.id)

    try:
        print("📂 Loading dataset (dashboard):", dataset.file_path)

        df = load_dataset(dataset.file_path)

        print("✅ Dataset loaded (dashboard):", df.shape)

        # CACHING
        df_hash = get_df_hash(df)
        df_json = df.to_json(orient="split", date_format="iso")

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
        print("⚠️ DASHBOARD RUNTIME ERROR:", str(e))
        raise HTTPException(400, str(e))

    except Exception as e:
        print("🔥 DASHBOARD ERROR:", str(e))
        raise HTTPException(500, f"Dashboard error: {str(e)}")