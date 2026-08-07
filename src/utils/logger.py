from pathlib import Path
import pandas as pd
from datetime import datetime


LOG_FILE = Path("logs/predictions.csv")


def log_prediction(payload, result):

    LOG_FILE.parent.mkdir(exist_ok=True)

    row = {

        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),

        "decision":
            result["decision"]["status"],

        "risk_score":
            result["risk_score"],

        "confidence":
            result["confidence"],

        "response_time_ms":
            result.get("response_time_ms"),

        "income":
            payload.get("AMT_INCOME_TOTAL"),

        "credit":
            payload.get("AMT_CREDIT"),

        "age":
            abs(payload.get("DAYS_BIRTH", 0)) / 365,

        "children":
            payload.get("CNT_CHILDREN"),

        "active_contracts":
            payload.get("active_contracts")
    }

    df = pd.DataFrame([row])

    if LOG_FILE.exists():

        df.to_csv(
            LOG_FILE,
            mode="a",
            header=False,
            index=False
        )

    else:

        df.to_csv(
            LOG_FILE,
            index=False
        )