import json
from pathlib import Path


def load_model_metadata():

    path = Path(
        "../artifacts/metadata/model_metadata.json"
    )

    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)