
import pandas as pd

from app.ml.data.prepare_multi_stock_dataset import (
    prepare_multi_stock_dataset
)


def analyze_target_distribution():

    df = prepare_multi_stock_dataset()

    print("\nOverall Target Distribution")
    print("=" * 55)

    print(
        df["target_return"].describe().to_string()
    )

    positive = (df["target_return"] > 0).sum()
    negative = (df["target_return"] < 0).sum()
    zero = (df["target_return"] == 0).sum()

    total = len(df)

    print("\nReturn Direction Distribution")
    print("=" * 55)

    print(f"Positive returns: {positive} ({positive / total:.2%})")
    print(f"Negative returns: {negative} ({negative / total:.2%})")
    print(f"Zero returns: {zero} ({zero / total:.2%})")

    print("\nStock-wise Target Statistics")
    print("=" * 55)

    stock_stats = (
        df.groupby("symbol")["target_return"]
        .agg([
            "count",
            "mean",
            "median",
            "std",
            "min",
            "max"
        ])
    )

    print(stock_stats.to_string())


if __name__ == "__main__":
    analyze_target_distribution()
