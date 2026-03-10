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
        corr = numeric_df.corr().fillna(0)

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

    # Convert numeric-like strings to numbers
    for col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="ignore")

    # Remove duplicates
    before = len(df)
    df = df.drop_duplicates()
    after = len(df)

    report["duplicates_removed"] = before - after

    filled_values = 0

    # Numeric columns
    numeric_cols = df.select_dtypes(include=["number"]).columns

    for col in numeric_cols:

        missing = df[col].isnull().sum()

        if missing > 0:
            df.loc[:, col] = df[col].fillna(df[col].mean())
            filled_values += int(missing)

    # Categorical columns
    categorical_cols = df.select_dtypes(include=["object"]).columns

    for col in categorical_cols:

        missing = df[col].isnull().sum()

        if missing > 0:
            df.loc[:, col] = df[col].fillna("Unknown")
            filled_values += int(missing)

    # Datetime columns
    datetime_cols = df.select_dtypes(include=["datetime64"]).columns

    for col in datetime_cols:

        missing = df[col].isnull().sum()

        if missing > 0:
            df.loc[:, col] = df[col].fillna(method="ffill")
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

    numeric_df = df.select_dtypes(include=["number"])

    if not numeric_df.empty:

        histograms = {}

        for col in numeric_df.columns:

            values = df[col].dropna().tolist()[:1000]

            histograms[col] = {
                "values": values
            }

        charts["histograms"] = histograms

    if len(numeric_df.columns) > 1:
        charts["correlation_matrix"] = numeric_df.corr().to_dict()

    if not numeric_df.empty:

        target = numeric_df.columns[-1]

        charts["trend"] = {
            "column": target,
            "values": numeric_df[target].tolist()[:1000]
        }

    return charts



# KPI GENERATION


def generate_kpis(df):

    numeric_df = df.select_dtypes(include=["number"])

    if numeric_df.empty:
        raise RuntimeError("No numeric columns available for KPI generation")

    kpis = {}

    for col in numeric_df.columns:
        kpis[f"average_{col}"] = round(df[col].mean(), 2)

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

    numeric_df = df.select_dtypes(include=["number"])

    if numeric_df.empty:
        raise RuntimeError("No numeric columns available for anomaly detection")

    model = IsolationForest(
        contamination=0.03,
        random_state=42,
        n_estimators=100
    )

    predictions = model.fit_predict(numeric_df)

    anomalies = numeric_df[predictions == -1]

    anomaly_rows = anomalies.index.tolist()

    results = []

    for idx in anomaly_rows:

        results.append({
            "row_index": int(idx),
            "values": df.iloc[idx].to_dict()
        })

    return {
        "total_anomalies": len(results),
        "anomalies": results[:10]
    }



# DASHBOARD GENERATOR


def generate_dashboard(df):

    dashboard = {}

    dashboard["kpis"] = generate_kpis(df)
    dashboard["charts"] = generate_charts(df)
    dashboard["insights"] = generate_insights(df)
    dashboard["forecast"] = generate_forecast(df)
    dashboard["anomalies"] = detect_anomalies(df)

    return dashboard