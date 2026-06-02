"""Utility functions for data loading and preprocessing."""
import gc
from pathlib import Path

import pandas as pd

from config import FEATURE_DEFINITIONS


def load_feature_definitions() -> pd.DataFrame:
    """Load feature definitions table."""
    return pd.read_csv(FEATURE_DEFINITIONS)


def reduce_memory_usage(df: pd.DataFrame) -> pd.DataFrame:
    """Downcast numeric columns to reduce memory footprint."""
    start_mem = df.memory_usage().sum() / 1024**2
    print(f"Memory usage before: {start_mem:.2f} MB")

    for col in df.columns:
        col_type = df[col].dtype
        if pd.api.types.is_integer_dtype(col_type):
            c_min, c_max = df[col].min(), df[col].max()
            if c_min > pd.api.types.iinfo("int8").min and c_max < pd.api.types.iinfo("int8").max:
                df[col] = df[col].astype("int8")
            elif c_min > pd.api.types.iinfo("int16").min and c_max < pd.api.types.iinfo("int16").max:
                df[col] = df[col].astype("int16")
            elif c_min > pd.api.types.iinfo("int32").min and c_max < pd.api.types.iinfo("int32").max:
                df[col] = df[col].astype("int32")
            else:
                df[col] = df[col].astype("int64")
        elif pd.api.types.is_float_dtype(col_type):
            c_min, c_max = df[col].min(), df[col].max()
            if c_min > pd.api.types.finfo("float16").min and c_max < pd.api.types.finfo("float16").max:
                df[col] = df[col].astype("float16")
            elif c_min > pd.api.types.finfo("float32").min and c_max < pd.api.types.finfo("float32").max:
                df[col] = df[col].astype("float32")
            else:
                df[col] = df[col].astype("float64")

    end_mem = df.memory_usage().sum() / 1024**2
    print(f"Memory usage after: {end_mem:.2f} MB")
    print(f"Reduced by {(start_mem - end_mem) / start_mem * 100:.1f}%")
    return df


def load_parquet_files(directory: Path, prefix: str = None) -> dict[str, pd.DataFrame]:
    """Load all parquet files from a directory into a dictionary.

    Args:
        directory: Path to directory containing .parquet files.
        prefix: Optional prefix filter for filenames.

    Returns:
        Dictionary mapping filename (without extension) to DataFrame.
    """
    files = sorted(directory.glob("*.parquet"))
    if prefix:
        files = [f for f in files if f.stem.startswith(prefix)]

    data = {}
    for f in files:
        print(f"Loading {f.name} ...")
        data[f.stem] = pd.read_parquet(f)
        gc.collect()
    return data


def get_base_table(train_dir: Path, test_dir: Path) -> pd.DataFrame:
    """Concatenate train and test base tables with a marker column."""
    train_base = pd.read_parquet(train_dir / "train_base.parquet")
    test_base = pd.read_parquet(test_dir / "test_base.parquet")
    train_base["split"] = "train"
    test_base["split"] = "test"
    return pd.concat([train_base, test_base], ignore_index=True)
