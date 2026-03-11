import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest



# DATASET PROFILE


def generate_profile(df: pd.DataFrame):

    profile = {}

    # Basic dataset info
    profile["rows"] = int(df.shape[0])
    profile["columns"] = int(df.shape[1])

    # Column data types
    profile["column_types"] = {
        col: str(dtype) for col, dtype in df.dtypes.items()
    }

    # Missing values count
    missing_counts = df.isnull().sum()

    profile["missing_values"] = {
        col: int(count) for col, count in missing_counts.items()
    }

    # Missing percentage
    profile["missing_percent"] = {
        col: round((count / len(df)) * 100, 2)
        for col, count in missing_counts.items()
    }

    # Numeric columns
    numeric_df = df.select_dtypes(include=["number"])

    if not numeric_df.empty:

        stats = numeric_df.describe()

        # Numeric summary
        profile["numeric_summary"] = {
            col: {
                "mean": round(float(stats.loc["mean", col]), 4),
                "min": round(float(stats.loc["min", col]), 4),
                "max": round(float(stats.loc["max", col]), 4),
                "std": round(float(stats.loc["std", col]), 4)
            }
            for col in numeric_df.columns
        }

        # Correlation matrix
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

    df = df.copy()

    report = {}

    # Replace infinite values
    df = df.replace([np.inf, -np.inf], np.nan)

    # Convert numeric-like columns
    for col in df.columns:

        if df[col].dtype == "object":

            converted = pd.to_numeric(df[col], errors="coerce")

            # Only replace if meaningful numeric data exists
            if converted.notnull().sum() > 0:
                df[col] = converted

    # Detect datetime columns
    for col in df.columns:

        try:
            parsed = pd.to_datetime(df[col], errors="ignore")

            if pd.api.types.is_datetime64_any_dtype(parsed):
                df[col] = parsed

        except Exception:
            pass

    # Remove duplicates
    before = len(df)
    df = df.drop_duplicates()
    report["duplicates_removed"] = before - len(df)

    filled_values = 0

    # Numeric columns
 
    numeric_cols = df.select_dtypes(include=["number"]).columns

    for col in numeric_cols:

        missing = df[col].isnull().sum()

        if missing > 0:

            median = df[col].median()

            if pd.isna(median):
                median = 0

            df[col] = df[col].fillna(median)

            filled_values += int(missing)

    # Categorical columns

    categorical_cols = df.select_dtypes(include=["object"]).columns

    for col in categorical_cols:

        missing = df[col].isnull().sum()

        if missing > 0:

            df[col] = df[col].fillna("Unknown")

            filled_values += int(missing)

    # Datetime columns

    datetime_cols = df.select_dtypes(include=["datetime"]).columns

    for col in datetime_cols:

        missing = df[col].isnull().sum()

        if missing > 0:

            df[col] = df[col].fillna(method="ffill")

            filled_values += int(missing)

    report["missing_values_filled"] = filled_values
    report["cleaned_rows"] = len(df)

    return df, report



# INSIGHTS GENERATION

def generate_insights(df):

    insights = []

    numeric_df = df.select_dtypes(include=["number"])

    summary = {
        "rows": df.shape[0],
        "columns": df.shape[1]
    }

    # Correlation insights
    if len(numeric_df.columns) > 1:

        corr_matrix = numeric_df.corr()

        for col in corr_matrix.columns:
            for idx in corr_matrix.index:

                if col != idx and abs(corr_matrix.loc[col, idx]) > 0.8:

                    insights.append(
                        f"{col} has strong correlation with {idx} ({round(corr_matrix.loc[col, idx],2)})"
                    )

    # Outlier detection
    for col in numeric_df.columns:

        mean = numeric_df[col].mean()
        std = numeric_df[col].std()

        outliers = numeric_df[
            (numeric_df[col] > mean + 3 * std) |
            (numeric_df[col] < mean - 3 * std)
        ]

        if len(outliers) > 0:
            insights.append(f"Column {col} contains {len(outliers)} potential outliers")

    # Average values
    for col in numeric_df.columns:
        insights.append(f"Average {col} is {round(numeric_df[col].mean(),2)}")

    return {
        "summary": summary,
        "insights": insights
    }



# CHART GENERATION
def generate_charts(df):

    charts = {}

    numeric_cols = df.select_dtypes(include=["number"]).columns.tolist()
    categorical_cols = df.select_dtypes(include=["object"]).columns.tolist()

    # HISTOGRAMS
    histograms = {}

    if numeric_cols:

        for col in numeric_cols[:4]:

            values = pd.to_numeric(df[col], errors="coerce").dropna().values

            if len(values) == 0:
                continue

            try:
                counts, bins = np.histogram(values, bins=10)
            except Exception:
                    continue

            histograms[col] = {
                "labels": [round(b, 2) for b in bins[:-1]],
                "values": counts.tolist()
            }

    charts["histograms"] = histograms


    # BAR CHARTS
    bars = {}

    if categorical_cols:

        for col in categorical_cols[:3]:

            counts = df[col].value_counts().head(10)

            bars[col] = {
                "labels": counts.index.tolist(),
                "values": counts.values.tolist()
            }

    charts["bars"] = bars


    # CORRELATION MATRIX
    if len(numeric_cols) > 1:

        corr = df[numeric_cols].corr()

        if not corr.empty:
            charts["correlation_matrix"] = corr.fillna(0).to_dict()


    # TREND
    if numeric_cols:

        target = next(
            (c for c in numeric_cols if "price" in c.lower() or "sales" in c.lower()),
            numeric_cols[0]
        )

        charts["trend"] = {
            "column": target,
            "values": pd.to_numeric(df[target], errors="coerce").dropna().tolist()[:1000]
        }

    return charts

# KPI GENERATION


def generate_kpis(df):

    kpis = {}

    numeric_cols = df.select_dtypes(include=["number"]).columns

    if len(numeric_cols) == 0:
        raise RuntimeError("No numeric columns available for KPI generation")

    # Averages
    for col in numeric_cols:

        value = df[col].mean()

        kpis[f"avg_{col}"] = round(value, 2) if not pd.isna(value) else None

    # Totals
    for col in numeric_cols:

        if any(word in col.lower() for word in ["sales", "revenue", "amount", "profit"]):

            value = df[col].sum()

            kpis[f"total_{col}"] = round(value, 2) if not pd.isna(value) else None

    # Unique IDs
    for col in df.columns:

        if "id" in col.lower():
            kpis[f"unique_{col}"] = int(df[col].nunique())

    kpis["total_rows"] = int(df.shape[0])
    kpis["total_columns"] = int(df.shape[1])

    return kpis


# FORECASTING


def generate_forecast(df, steps: int = 5):

    numeric_df = df.select_dtypes(include=["number"])

    if numeric_df.empty:
        raise RuntimeError("No numeric column available for forecasting")

    # Select most important numeric column
    target_col = numeric_df.mean().idxmax()

    series = numeric_df[target_col].dropna()

    if len(series) < 5:
        raise RuntimeError("Not enough data for forecasting")

    try:
        trend = np.polyfit(range(len(series)), series, 1)
    except Exception:
        raise RuntimeError("Forecasting failed due to unstable data")

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

    numeric_df = df.select_dtypes(include=["number"])

    # Handle datasets with no numeric columns
    if numeric_df.empty:
        return {
            "total_anomalies": 0,
            "anomalies": []
        }

    # Replace invalid values
    numeric_df = numeric_df.replace([np.inf, -np.inf], np.nan)

    # Fill missing values
    numeric_df = numeric_df.fillna(numeric_df.mean())

    # IsolationForest fails on tiny datasets
    if len(numeric_df) < 20:
        return {
            "total_anomalies": 0,
            "anomalies": []
        }

    model = IsolationForest(
        contamination=0.03,
        random_state=42,
        n_estimators=100
    )

    predictions = model.fit_predict(numeric_df)

    anomalies = numeric_df[predictions == -1]

    anomaly_rows = anomalies.index.tolist()

    results = []

    for idx in anomaly_rows[:10]:
        results.append({
            "row_index": int(idx),
            "values": df.iloc[idx].to_dict()
        })

    return {
        "total_anomalies": len(anomaly_rows),
        "anomalies": results
    }

# BUSINESS INSIGHTS

def generate_business_insights(df: pd.DataFrame, max_insights: int = 12):

    insights = []

    if df.empty:
        return insights

    numeric_cols = df.select_dtypes(include=["number"]).columns.tolist()
    categorical_cols = df.select_dtypes(include=["object"]).columns.tolist()

    # Remove ID-like columns
    categorical_cols = [
        col for col in categorical_cols
        if not col.lower().endswith("id") and "id" not in col.lower()
    ]


    # DATASET SIZE INSIGHT

    insights.append(
        f"Dataset contains {df.shape[0]} records across {df.shape[1]} columns."
    )


    # DOMINANT CATEGORY INSIGHTS

    for col in categorical_cols:

        value_counts = df[col].value_counts(dropna=True)

        if len(value_counts) == 0:
            continue

        top_value = value_counts.idxmax()
        top_share = value_counts.max() / len(df)

        if top_share > 0.4:
            insights.append(
                f"'{top_value}' dominates the '{col}' category ({round(top_share*100,1)}% of records)."
            )


    # NUMERIC RANGE INSIGHTS
  
    for col in numeric_cols:

        min_val = df[col].min()
        max_val = df[col].max()

        if pd.isna(min_val) or pd.isna(max_val):
            continue

        insights.append(
            f"'{col}' ranges from {round(min_val,2)} to {round(max_val,2)}."
        )


    # HIGH VARIANCE DETECTION
  
    for col in numeric_cols:

        std = df[col].std()
        mean = df[col].mean()

        if mean == 0 or pd.isna(std):
            continue

        if std / mean > 1:
            insights.append(
                f"'{col}' shows high variability relative to its average."
            )


    # CATEGORY PERFORMANCE VS NUMERIC
  
    for cat in categorical_cols:

        if df[cat].nunique() > 20:
            continue

        for num in numeric_cols:

            grouped = df.groupby(cat)[num].mean()

            if len(grouped) == 0:
                continue

            best_category = grouped.idxmax()
            best_value = grouped.max()

            insights.append(
                f"{best_category} has the highest average {num} ({round(best_value,2)})."
            )

    # CORRELATION INSIGHTS
 
    if len(numeric_cols) > 1:

        corr_matrix = df[numeric_cols].corr()

        for i in range(len(corr_matrix.columns)):
            for j in range(i + 1, len(corr_matrix.columns)):

                col1 = corr_matrix.columns[i]
                col2 = corr_matrix.columns[j]

                corr_val = corr_matrix.iloc[i, j]

                if abs(corr_val) > 0.65:

                    direction = "positive" if corr_val > 0 else "negative"

                    insights.append(
                        f"{col1} and {col2} show strong {direction} correlation ({round(corr_val,2)})."
                    )

    # LIMIT TOTAL INSIGHTS

    insights = insights[:max_insights]

    return insights   


# DASHBOARD GENERATION

def generate_dashboard(df):

    dashboard = {}

    try:
        dashboard["kpis"] = generate_kpis(df)
    except Exception:
        dashboard["kpis"] = {}

    try:
        dashboard["charts"] = generate_charts(df)
    except Exception:
        dashboard["charts"] = {}

    try:
        dashboard["forecast"] = generate_forecast(df)
    except Exception:
        dashboard["forecast"] = {"forecast": []}

    try:
        dashboard["anomalies"] = detect_anomalies(df)
    except Exception:
        dashboard["anomalies"] = {
            "total_anomalies": 0,
            "anomalies": []
        }

    try:
        statistical = generate_insights(df)
    except Exception:
        statistical = {"summary": {}, "insights": []}

    try:
        business = generate_business_insights(df)
    except Exception:
        business = []

    dashboard["insights"] = {
        "summary": statistical.get("summary", {}),
        "statistical_insights": statistical.get("insights", []),
        "business_insights": business
    }

    return dashboard