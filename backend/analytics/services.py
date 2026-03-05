import pandas as pd


def generate_profile(df: pd.DataFrame):

    profile = {}

    profile["rows"] = df.shape[0]
    profile["columns"] = df.shape[1]

    profile["column_types"] = {
        col: str(dtype) for col, dtype in df.dtypes.items()
    }

    profile["missing_values"] = df.isnull().sum().to_dict()

    numeric_df = df.select_dtypes(include=["number"])

    if not numeric_df.empty:
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