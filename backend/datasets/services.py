import pandas as pd
import numpy as np


def load_dataset(file_path: str):

    try:
        # LOAD FILE

        if file_path.endswith(".csv"):

            try:
                df = pd.read_csv(file_path)

            except UnicodeDecodeError:
                df = pd.read_csv(file_path, encoding="latin1")

        elif file_path.endswith((".xlsx", ".xls")):

            df = pd.read_excel(file_path, engine="openpyxl")

        else:
            raise ValueError("Unsupported file format")

        # CLEAN COLUMN NAMES

        df.columns = (
            df.columns
            .str.strip()
            .str.lower()
            .str.replace(" ", "_")
        )

        # CONVERT NUMERIC-LIKE COLUMNS

        for col in df.columns:

            if df[col].dtype == "object":

                converted = pd.to_numeric(df[col], errors="coerce")

                # Only replace if conversion actually produced numbers
                if converted.notna().sum() > 0:
                    df[col] = converted

        # DETECT DATETIME COLUMNS

        for col in df.columns:

            if df[col].dtype == "object":

                try:
                    parsed = pd.to_datetime(
                        df[col],
                        errors="coerce",
                        infer_datetime_format=True
                    )

                    # Only convert if at least some values were parsed
                    if parsed.notna().sum() > 0:
                        df[col] = parsed

                except Exception:
                    pass

        # REMOVE INFINITE VALUES

        df = df.replace([np.inf, -np.inf], np.nan)

        # PROTECT AGAINST HUGE DATASETS

        if df.shape[0] > 100000:
            df = df.sample(100000, random_state=42)

        # PROTECT AGAINST TOO MANY COLUMNS

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
        print("DATASET PREVIEW ERROR:", e)

        raise RuntimeError("Failed to generate dataset preview") from e