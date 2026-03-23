import pandas as pd
import numpy as np
import requests
from io import BytesIO


def load_dataset(file_path: str):

    try:
        # Handle URL (Supabase storage)
        if file_path.startswith("http"):
            response = requests.get(file_path)

            if response.status_code != 200:
                raise RuntimeError("Failed to fetch dataset")

            file_obj = BytesIO(response.content)

        else:
            file_obj = file_path

        # LOAD FILE
        if file_path.endswith(".csv"):
            try:
                df = pd.read_csv(file_obj)
            except UnicodeDecodeError:
                df = pd.read_csv(file_obj, encoding="latin1")

        elif file_path.endswith((".xlsx", ".xls")):
            df = pd.read_excel(file_obj, engine="openpyxl")

        else:
            raise ValueError("Unsupported file format")

        # CLEAN COLUMN NAMES
        df.columns = (
            df.columns
            .str.strip()
            .str.lower()
            .str.replace(" ", "_")
        )

        # CONVERT NUMERIC
        for col in df.columns:
            if df[col].dtype == "object":
                converted = pd.to_numeric(df[col], errors="coerce")
                if converted.notna().sum() > 0:
                    df[col] = converted

        # DATETIME DETECTION
        for col in df.columns:
            if df[col].dtype == "object":
                try:
                    parsed = pd.to_datetime(df[col], errors="coerce")
                    if parsed.notna().sum() > 0:
                        df[col] = parsed
                except:
                    pass

        # REMOVE INF
        df = df.replace([np.inf, -np.inf], np.nan)

        # LIMIT SIZE (SAFETY)
        if df.shape[0] > 100000:
            df = df.sample(100000, random_state=42)

        if df.shape[1] > 100:
            df = df.iloc[:, :100]

        return df

    except Exception as e:
        raise RuntimeError("Failed to process dataset") from e


def dataset_summary(df):
    return {
        "rows": int(df.shape[0]),
        "columns": int(df.shape[1])
    }


def dataset_preview(df, rows: int = 10):
    try:
        preview = df.head(rows).copy()
        preview = preview.replace([np.nan, np.inf, -np.inf], None)

        return {
            "columns": list(preview.columns),
            "dtypes": {col: str(dtype) for col, dtype in df.dtypes.items()},
            "rows": preview.to_dict(orient="records")
        }

    except Exception as e:
        raise RuntimeError("Failed to generate dataset preview") from e