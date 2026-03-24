import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
from functools import lru_cache
import hashlib

# VALIDATION + CACHING

def validate_dataframe(df):
    if df is None or df.empty:
        raise RuntimeError("Dataset is empty or invalid")


def get_df_hash(df):
    return hashlib.md5(
        pd.util.hash_pandas_object(df, index=True).values
    ).hexdigest()


# DATASET PROFILE

def generate_profile(df: pd.DataFrame):

    validate_dataframe(df)

    profile = {}

    profile["rows"] = int(df.shape[0])
    profile["columns"] = int(df.shape[1])

    profile["column_types"] = {
        col: str(dtype) for col, dtype in df.dtypes.items()
    }

    missing_counts = df.isnull().sum()

    profile["missing_values"] = {
        col: int(count) for col, count in missing_counts.items()
    }

    profile["missing_percent"] = {
        col: round((count / len(df)) * 100, 2)
        for col, count in missing_counts.items()
    }

    numeric_df = df.select_dtypes(include=["number"])

    if not numeric_df.empty:

        stats = numeric_df.describe()

        profile["numeric_summary"] = {
            col: {
                "mean": round(float(stats.loc["mean", col]), 4),
                "min": round(float(stats.loc["min", col]), 4),
                "max": round(float(stats.loc["max", col]), 4),
                "std": round(float(stats.loc["std", col]), 4)
            }
            for col in numeric_df.columns
        }

        corr = numeric_df.corr(numeric_only=True).fillna(0)

        profile["correlation"] = {
            col: {
                subcol: round(float(value), 4)
                for subcol, value in corr[col].items()
            }
            for col in corr.columns
        }

    else:
        profile["numeric_summary"] = {}
        profile["correlation"] = {}

    return profile


# DATA CLEANING

def clean_dataset(df):

    validate_dataframe(df)

    df = df.copy()
    report = {}

    df = df.replace([np.inf, -np.inf], np.nan)

    # Convert numeric-like columns
    for col in df.columns:
        if df[col].dtype == "object":
            converted = pd.to_numeric(df[col], errors="coerce")
            if converted.notnull().sum() > 0:
                df[col] = converted

    # FIXED datetime parsing
    for col in df.columns:
        try:
            parsed = pd.to_datetime(df[col], errors="coerce")
            if parsed.notna().sum() > 0:
                df[col] = parsed
        except:
            pass

    before = len(df)
    df = df.drop_duplicates()
    report["duplicates_removed"] = before - len(df)

    filled_values = 0

    # Numeric
    for col in df.select_dtypes(include=["number"]).columns:
        missing = df[col].isnull().sum()
        if missing > 0:
            median = df[col].median()
            if pd.isna(median):
                median = 0
            df[col] = df[col].fillna(median)
            filled_values += int(missing)

    # Categorical
    for col in df.select_dtypes(include=["object"]).columns:
        missing = df[col].isnull().sum()
        if missing > 0:
            df[col] = df[col].fillna("Unknown")
            filled_values += int(missing)

    # Datetime
    for col in df.select_dtypes(include=["datetime"]).columns:
        missing = df[col].isnull().sum()
        if missing > 0:
            df[col] = df[col].ffill()
            filled_values += int(missing)

    report["missing_values_filled"] = filled_values
    report["cleaned_rows"] = len(df)

    return df, report


# INSIGHTS GENERATION

def generate_insights(df):

    validate_dataframe(df)

    insights = []

    numeric_df = df.select_dtypes(include=["number"])
    numeric_df = numeric_df[
        [col for col in numeric_df.columns if "id" not in col.lower()]
    ]

    numeric_df = numeric_df.replace([np.inf, -np.inf], np.nan)

    summary = {
        "rows": int(df.shape[0]),
        "columns": int(df.shape[1])
    }

    # Correlation insights
    if len(numeric_df.columns) > 1:

        corr_matrix = numeric_df.corr(numeric_only=True)

        checked_pairs = set()

        for col in corr_matrix.columns:
            for idx in corr_matrix.index:

                if col == idx:
                    continue

                pair = tuple(sorted([col, idx]))

                if pair in checked_pairs:
                    continue

                corr_val = corr_matrix.loc[col, idx]

                if abs(corr_val) > 0.8:
                    direction = "positive" if corr_val > 0 else "negative"

                    insights.append(
                        f"{col} and {idx} show strong {direction} correlation ({round(corr_val,2)})."
                    )

                    checked_pairs.add(pair)

    # Outliers
    for col in numeric_df.columns:

        series = pd.to_numeric(numeric_df[col], errors="coerce").dropna()

        if len(series) < 5:
            continue

        mean = series.mean()
        std = series.std()

        outliers = series[
            (series > mean + 3 * std) |
            (series < mean - 3 * std)
        ]

        if len(outliers) > 0:

            percentage = (len(outliers) / len(series)) * 100

            insights.append(
                f"{len(outliers)} outliers detected in '{col}' ({round(percentage,1)}% of data)."
            )

    # Averages
    for col in numeric_df.columns[:5]:
        value = numeric_df[col].mean()
        if not pd.isna(value):
            insights.append(
                f"Average {col} is {round(value,2)}."
            )

    return {
        "summary": summary,
        "insights": insights
    }


# CHART GENERATION 

def generate_charts(df):

    validate_dataframe(df)

    charts = {}

    numeric_cols = df.select_dtypes(include=["number"]).columns.tolist()

    categorical_cols = [
        col for col in df.select_dtypes(include=["object"]).columns
        if "id" not in col.lower()
    ]

    # HISTOGRAMS
    histograms = {}

    for col in numeric_cols[:4]:

        try:
            values = pd.to_numeric(df[col], errors="coerce")
            values = values.replace([np.inf, -np.inf], np.nan).dropna()

            if len(values) > 10000:
                values = values.sample(10000)

            if len(values) == 0:
                continue

            counts, bins = np.histogram(values, bins=10)

            histograms[col] = {
                "labels": [round(b, 2) for b in bins[:-1]],
                "values": counts.tolist()
            }

        except:
            continue

    charts["histograms"] = histograms

    # BAR CHARTS
    bars = {}

    for col in categorical_cols[:3]:
        try:
            counts = df[col].astype(str).value_counts().head(10)

            if counts.empty:
                continue

            bars[col] = {
                "labels": counts.index.tolist(),
                "values": counts.values.tolist()
            }

        except:
            continue

    charts["bars"] = bars

    # CORRELATION MATRIX
    if len(numeric_cols) > 1:
        try:
            corr = df[numeric_cols].corr(numeric_only=True)

            if not corr.empty:
                charts["correlation_matrix"] = corr.fillna(0).to_dict()

        except:
            pass

    # TREND
    if numeric_cols:

        try:
            priority_keywords = ["sales", "revenue", "amount", "price", "profit"]

            target = None

            for col in numeric_cols:
                if any(k in col.lower() for k in priority_keywords):
                    target = col
                    break

            if target is None:
                target = numeric_cols[0]

            values = pd.to_numeric(df[target], errors="coerce")
            values = values.replace([np.inf, -np.inf], np.nan).dropna()

            if not values.empty:
                charts["trend"] = {
                    "column": target,
                    "values": values.head(300).tolist()
                }

        except:
            pass

    return charts


# KPI GENERATION

def generate_kpis(df):

    validate_dataframe(df)

    kpis = {}

    numeric_cols = df.select_dtypes(include=["number"]).columns

    if len(numeric_cols) == 0:
        raise RuntimeError("No numeric columns available for KPI generation")

    for col in numeric_cols:
        value = df[col].mean()
        kpis[f"avg_{col}"] = round(value, 2) if not pd.isna(value) else None

    for col in numeric_cols:
        if any(word in col.lower() for word in ["sales", "revenue", "amount", "profit"]):
            value = df[col].sum()
            kpis[f"total_{col}"] = round(value, 2) if not pd.isna(value) else None

    for col in df.columns:
        if "id" in col.lower():
            kpis[f"unique_{col}"] = int(df[col].nunique())

    kpis["total_rows"] = int(df.shape[0])
    kpis["total_columns"] = int(df.shape[1])

    return kpis


# FORECASTING 

def generate_forecast(df, steps: int = 5):

    validate_dataframe(df)

    numeric_df = df.select_dtypes(include=["number"])

    if numeric_df.empty:
        raise RuntimeError("No numeric column available for forecasting")

    numeric_df = numeric_df.replace([np.inf, -np.inf], np.nan)

    priority_keywords = ["sales", "revenue", "amount", "price", "profit"]

    target_col = None

    for col in numeric_df.columns:
        if any(k in col.lower() for k in priority_keywords):
            target_col = col
            break

    if target_col is None:
        target_col = numeric_df.var().sort_values(ascending=False).index[0]

    series = pd.to_numeric(numeric_df[target_col], errors="coerce").dropna()

    if len(series) < 5:
        raise RuntimeError("Not enough data for forecasting")

    if series.nunique() < 2:
        raise RuntimeError("Forecasting failed: data has no variation")

    trend = np.polyfit(range(len(series)), series, 1)

    predictions = []

    for i in range(steps):
        next_index = len(series) + i
        predicted_value = trend[0] * next_index + trend[1]

        predictions.append({
            "step": i + 1,
            "predicted_value": round(float(predicted_value), 2)
        })

    return {
        "target_column": target_col,
        "forecast": predictions
    }


# ANOMALY DETECTION 

def detect_anomalies(df):

    validate_dataframe(df)

    numeric_df = df.select_dtypes(include=["number"])

    if numeric_df.empty:
        return {"total_anomalies": 0, "anomalies": []}

    numeric_df = numeric_df.replace([np.inf, -np.inf], np.nan)
    numeric_df = numeric_df.fillna(numeric_df.mean())
    numeric_df = numeric_df.fillna(0)

    if len(numeric_df) < 20:
        return {"total_anomalies": 0, "anomalies": []}

    model = IsolationForest(contamination=0.03, random_state=42)

    predictions = model.fit_predict(numeric_df)

    anomalies = numeric_df[predictions == -1]

    return {
        "total_anomalies": len(anomalies),
        "anomalies": [
            {"row_index": int(idx), "values": df.iloc[idx].to_dict()}
            for idx in anomalies.index[:10]
        ]
    }


# BUSINESS INSIGHTS GENERATION

def generate_business_insights(df: pd.DataFrame, max_insights: int = 12):

    if df is None or df.empty:
        return []

    insights = []

    numeric_cols = df.select_dtypes(include=["number"]).columns.tolist()
    categorical_cols = df.select_dtypes(include=["object"]).columns.tolist()

    categorical_cols = [
        col for col in categorical_cols
        if not col.lower().endswith("id") and "id" not in col.lower()
    ]

    total_rows = df.shape[0]
    total_cols = df.shape[1]

    insights.append(
        f"Dataset contains {total_rows} records and {total_cols} columns "
        f"({len(numeric_cols)} numeric, {len(categorical_cols)} categorical)."
    )

    # Dominant category
    for col in categorical_cols:
        try:
            value_counts = df[col].value_counts(dropna=True)

            if value_counts.empty:
                continue

            top_value = value_counts.idxmax()
            top_share = value_counts.max() / len(df)

            if top_share > 0.4:
                insights.append(
                    f"'{top_value}' dominates '{col}' ({round(top_share*100,1)}%)."
                )
        except:
            continue

    # Numeric range
    for col in numeric_cols:
        series = pd.to_numeric(df[col], errors="coerce")

        if series.dropna().empty:
            continue

        insights.append(
            f"'{col}' ranges from {round(series.min(),2)} to {round(series.max(),2)}."
        )

    # High variance
    for col in numeric_cols:
        series = pd.to_numeric(df[col], errors="coerce")

        mean = series.mean()
        std = series.std()

        if mean and std and std / mean > 1:
            insights.append(
                f"'{col}' shows high variability."
            )

    # Category vs numeric
    for cat in categorical_cols:
        if df[cat].nunique() > 20:
            continue

        for num in numeric_cols:
            try:
                grouped = df.groupby(cat)[num].mean()

                if grouped.empty:
                    continue

                best_category = grouped.idxmax()
                best_value = grouped.max()

                insights.append(
                    f"{best_category} has highest avg {num} ({round(best_value,2)})."
                )
            except:
                continue

    # Correlation
    if len(numeric_cols) > 1:
        try:
            corr = df[numeric_cols].corr(numeric_only=True)

            for i in range(len(corr.columns)):
                for j in range(i + 1, len(corr.columns)):

                    val = corr.iloc[i, j]

                    if abs(val) > 0.65:
                        direction = "positive" if val > 0 else "negative"

                        insights.append(
                            f"{corr.columns[i]} and {corr.columns[j]} show {direction} correlation ({round(val,2)})."
                        )
        except:
            pass

    return insights[:max_insights]


# DASHBOARD (CACHED)

@lru_cache(maxsize=10)
def cached_dashboard(df_hash, df_json):
    try:
        df = pd.read_json(df_json, orient="split", convert_dates=False)
    except Exception as e:
        print("🔥 JSON LOAD ERROR:", str(e))
        raise RuntimeError(f"Dashboard JSON load failed: {str(e)}")

    return generate_dashboard(df)


def generate_dashboard(df):

    validate_dataframe(df)

    dashboard = {}

    try:
        dashboard["kpis"] = generate_kpis(df)
    except:
        dashboard["kpis"] = {}

    try:
        dashboard["charts"] = generate_charts(df)
    except:
        dashboard["charts"] = {}

    try:
        dashboard["forecast"] = generate_forecast(df)
    except:
        dashboard["forecast"] = {"forecast": []}

    try:
        dashboard["anomalies"] = detect_anomalies(df)
    except:
        dashboard["anomalies"] = {"total_anomalies": 0, "anomalies": []}

    try:
        statistical = generate_insights(df)
    except:
        statistical = {"summary": {}, "insights": []}

    try:
        business = generate_business_insights(df)
    except:
        business = []

    dashboard["insights"] = {
        "summary": statistical.get("summary", {}),
        "statistical_insights": statistical.get("insights", []),
        "business_insights": business
    }

    return dashboard