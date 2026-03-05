import pandas as pd


def load_dataset(file_path: str):
    try:
        if file_path.endswith(".csv"):
            df = pd.read_csv(file_path)

        elif file_path.endswith(".xlsx") or file_path.endswith(".xls"):
            df = pd.read_excel(file_path)

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
        preview = df.head(rows)

        return {
            "columns": list(preview.columns),
            "dtypes": {col: str(dtype) for col, dtype in preview.dtypes.items()},
            "rows": preview.to_dict(orient="records")
        }

    except Exception as e:
        raise RuntimeError("Failed to generate dataset preview") from e