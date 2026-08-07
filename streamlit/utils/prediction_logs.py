from pathlib import Path
import pandas as pd


BASE_DIR = Path(__file__).resolve().parents[2]

LOG_FILE = (
    BASE_DIR /
    "logs" /
    "predictions.csv"
)


def load_prediction_logs():

    if not LOG_FILE.exists():
        return pd.DataFrame()


    return pd.read_csv(LOG_FILE)