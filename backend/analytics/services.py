import pandas as pd 
import numpy as np 


#generate a profile of the dataset with basic stats and correlations
def generate_profile(df: pd.DataFrame):

    profile = {}

    profile["rows"] = df.shape[0]  # number of rows
    profile["columns"] = df.shape[1]   # number of columns

    profile["column_types"] = {
        col: str(dtype) for col, dtype in df.dtypes.items()   # data types of each column
    }

    profile["missing_values"] = df.isnull().sum().to_dict()   # count of missing values per column

    numeric_df = df.select_dtypes(include=["number"])     # subset of numeric columns for stats and correlations

    if not numeric_df.empty:                             # if there are numeric columns, calculate stats and correlations
        stats = numeric_df.describe().to_dict()

        profile["numeric_summary"] = {
            col: {
                "mean": stats[col]["mean"],
                "min": stats[col]["min"],
                "max": stats[col]["max"]
            }
            for col in stats
        }

        profile["correlation_matrix"] = numeric_df.corr().to_dict()

    else:
        profile["numeric_summary"] = {}
        profile["correlation_matrix"] = {}

    return profile


def generate_insights(df):

    insights = []

    # Missing values
    missing = df.isnull().sum()

    for col, count in missing.items():
        if count > 0:
            insights.append(f"Column '{col}' contains {count} missing values.")

    # Cardinality insights
    for col in df.columns:
        unique_count = df[col].nunique()
        if unique_count > 50:
            insights.append(
                f"Column '{col}' has high cardinality with {unique_count} unique values."
            )

    # Numeric insights
    numeric_df = df.select_dtypes(include=["number"])

    if not numeric_df.empty:

        means = numeric_df.mean()
        top_col = means.idxmax()

        insights.append(
            f"Column '{top_col}' has the highest average value ({means[top_col]:.2f})."
        )

        for col in numeric_df.columns:
            col_min = numeric_df[col].min()
            col_max = numeric_df[col].max()

            insights.append(
                f"Column '{col}' ranges from {col_min} to {col_max}."
            )

        # Correlation insight
        corr = numeric_df.corr()

        for col in corr.columns:
            for row in corr.index:
                if col != row and abs(corr.loc[row, col]) > 0.8:
                    insights.append(
                        f"Strong correlation detected between '{row}' and '{col}'."
                    )

    # Categorical insights
    categorical = df.select_dtypes(include=["object"])

    for col in categorical.columns:
        top_value = df[col].value_counts().idxmax()

        insights.append(
            f"Most frequent value in '{col}' is '{top_value}'."
        )

    return insights 


def generate_forecast(df, steps: int = 5):

    numeric_df = df.select_dtypes(include=["number"])

    if numeric_df.empty:
        raise RuntimeError("No numeric column available for forecasting")

    # Select first numeric column
    target_col = numeric_df.columns[0]

    series = numeric_df[target_col].dropna()

    if len(series) < 5:
        raise RuntimeError("Not enough data for forecasting")

    # Simple trend calculation
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

def clean_dataset(df):

    report = {}

    # Remove duplicates
    before = len(df)
    df = df.drop_duplicates()
    after = len(df)

    report["duplicates_removed"] = before - after

    # Fill numeric missing values
    numeric_cols = df.select_dtypes(include=["number"]).columns

    for col in numeric_cols:
        if df[col].isnull().sum() > 0:
            df[col] = df[col].fillna(df[col].mean())

    # Fill categorical missing values
    categorical_cols = df.select_dtypes(include=["object"]).columns

    for col in categorical_cols:
        if df[col].isnull().sum() > 0:
            df[col] = df[col].fillna("Unknown")

    report["cleaned_rows"] = len(df)

    return df, report 

def generate_charts(df):

    charts = {}

    # Histogram data
    numeric_df = df.select_dtypes(include=["number"])

    if not numeric_df.empty:

        histograms = {}

        for col in numeric_df.columns:
            histograms[col] = {
                "values": df[col].dropna().tolist()
            }

        charts["histograms"] = histograms

    # Correlation heatmap
    if len(numeric_df.columns) > 1:
        charts["correlation_matrix"] = numeric_df.corr().to_dict()

    # Trend data (first numeric column)
    if not numeric_df.empty:
        target = numeric_df.columns[0]

        charts["trend"] = {
            "column": target,
            "values": numeric_df[target].tolist()
        }

    return charts  


def generate_insights(df):

    insights = [] 

    numeric_df = df.select_dtypes(include=["number"]) 

    #summary  
    summary = {
        "rows": df.shape[0],
        "columns": df.shape[1]
    } 

    #Correlation insights 
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