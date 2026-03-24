import pandas as pd
import numpy as np
import requests
from io import BytesIO
from urllib.parse import unquote   


def load_dataset(file_path: str):

    try:
        print("📂 Loading dataset from:", file_path)

        # Handle URL (Supabase storage)
        if file_path.startswith("http"):
            try:
                decoded_url = unquote(file_path)   
                print("🌐 Fetching URL:", decoded_url)

                response = requests.get(decoded_url, timeout=10)

                if response.status_code != 200:
                    raise RuntimeError(
                        f"Failed to fetch dataset: {response.status_code}"
                    )

                file_obj = BytesIO(response.content)

                print("✅ Remote file fetched successfully")

            except Exception as e:
                print("🔥 HTTP FETCH ERROR:", str(e))
                raise RuntimeError(f"Failed to fetch dataset: {str(e)}")

        else:
            file_obj = file_path

        # LOAD FILE
        if file_path.endswith(".csv"):
            try:
                df = pd.read_csv(file_obj)
            except Exception:   
                file_obj.seek(0)   # reset pointer
                df = pd.read_csv(file_obj, encoding="latin1")

        elif file_path.endswith((".xlsx", ".xls")):
            df = pd.read_excel(file_obj, engine="openpyxl")

        else:
            raise ValueError("Unsupported file format")

        print("✅ File loaded. Shape:", df.shape)

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
                except Exception:
                    pass

        # REMOVE INF
        df = df.replace([np.inf, -np.inf], np.nan)

        # LIMIT SIZE (SAFETY)
        if df.shape[0] > 100000:
            print("⚠️ Large dataset detected, sampling 100000 rows")
            df = df.sample(100000, random_state=42)

        if df.shape[1] > 100:
            print("⚠️ Too many columns, limiting to 100")
            df = df.iloc[:, :100]

        return df

    except Exception as e:
        print("🔥 LOAD DATASET ERROR:", str(e))
        raise RuntimeError(f"Failed to process dataset: {str(e)}")


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
        print("🔥 PREVIEW ERROR:", str(e))
        raise RuntimeError(f"Failed to generate dataset preview: {str(e)}")