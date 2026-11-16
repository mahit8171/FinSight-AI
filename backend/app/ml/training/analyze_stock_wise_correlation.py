
import pandas as pd

from app.ml.data.prepare_multi_stock_dataset import prepare_multi_stock_dataset
from app.ml.data.prepare_dataset import FEATURE_COLUMNS


def analyze_stock_wise_correlation():

    df = prepare_multi_stock_dataset()

    for symbol, stock_df in df.groupby("symbol"):

        correlation = (
            stock_df[FEATURE_COLUMNS + ["target_return"]]
            .corr(numeric_only=True)["target_return"]
            .drop("target_return")
            .sort_values(key=abs, ascending=False)
        )

        print(f"\n{symbol}")
        print("-" * 40)
        print(correlation.head(5).to_string())


if __name__ == "__main__":
    analyze_stock_wise_correlation()

