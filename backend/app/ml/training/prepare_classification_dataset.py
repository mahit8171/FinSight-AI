
import pandas as pd

from app.ml.data.prepare_multi_stock_dataset import (
    prepare_multi_stock_dataset
)


def prepare_classification_dataset():

    df = prepare_multi_stock_dataset()

    # Positive return = 1, otherwise = 0
    df["target_direction"] = (
        df["target_return"] > 0
    ).astype(int)

    print("\nClassification Target Distribution")
    print("=" * 50)

    print(
        df["target_direction"]
        .value_counts()
        .sort_index()
    )

    print("\nClass Distribution Percentage")
    print("=" * 50)

    print(
        df["target_direction"]
        .value_counts(normalize=True)
        .sort_index()
    )

    return df


if __name__ == "__main__":
    prepare_classification_dataset()
