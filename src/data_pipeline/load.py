from pathlib import Path
import pandas as pd


def save_dataframe(
    df: pd.DataFrame,
    output_path: str
):

    Path(output_path).parent.mkdir(
        parents=True,
        exist_ok=True
    )

    df.to_parquet(
        output_path,
        index=False
    )

    print(
        f"Dataset saved -> {output_path}"
    )