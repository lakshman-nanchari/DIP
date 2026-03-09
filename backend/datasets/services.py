import pandas as pd
import numpy as np

def load_dataset(file_path: str):

    try:

        if file_path.endswith(".csv"):
            df = pd.read_csv(file_path)

        elif file_path.endswith(".xlsx") or file_path.endswith(".xls"):
            df = pd.read_excel(file_path, engine="openpyxl")

        else:
            raise ValueError("Unsupported file format")

        return df

    except Exception as e:
        raise RuntimeError("Failed to process dataset") from e


def dataset_summary(df):
    return {
        "rows": df.shape[0],
        "columns": df.shape[1]
    }


def dataset_preview(df, rows: int = 10):

    try:

        preview = df.head(rows).copy()

        # Convert NaN to None
        preview = preview.replace({np.nan: None})

        # Convert all values to JSON-safe types
        preview = preview.astype(str)

        return {
            "columns": list(preview.columns),
            "dtypes": {col: str(dtype) for col, dtype in df.dtypes.items()},
            "rows": preview.to_dict(orient="records")
        }

    except Exception as e:
        print("DATASET PREVIEW ERROR:", e)
        raise RuntimeError("Failed to generate dataset preview") from e