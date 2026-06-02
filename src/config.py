"""Project configuration and paths."""
from pathlib import Path

# Base paths
PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT.parent / "home_credit_crms_2024"

# Data subdirectories
PARQUET_DIR = DATA_DIR / "parquet_files"
CSV_DIR = DATA_DIR / "csv_files"

# Train / Test paths
TRAIN_PARQUET = PARQUET_DIR / "train"
TEST_PARQUET = PARQUET_DIR / "test"
TRAIN_CSV = CSV_DIR / "train"
TEST_CSV = CSV_DIR / "test"

# Feature definitions
FEATURE_DEFINITIONS = DATA_DIR / "feature_definitions.csv"

# Outputs
MODELS_DIR = PROJECT_ROOT / "models"
REPORTS_DIR = PROJECT_ROOT / "reports"

# Create output directories if not exist
MODELS_DIR.mkdir(exist_ok=True)
REPORTS_DIR.mkdir(exist_ok=True)

# Random seed for reproducibility
RANDOM_STATE = 42

# Target column name
TARGET_COL = "target"

# Key ID columns
CASE_ID = "case_id"
WEEK_NUM = "WEEK_NUM"
MONTH = "month"
