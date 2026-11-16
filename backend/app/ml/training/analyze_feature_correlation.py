
import pandas as pd

from app.ml.data.prepare_multi_stock_dataset import prepare_multi_stock_dataset
from app.ml.data.prepare_dataset import FEATURE_COLUMNS


def analyze_feature_correlation():

    df = prepare_multi_stock_dataset()

    correlation = (
        df[FEATURE_COLUMNS + ["target_return"]]
        .corr(numeric_only=True)["target_return"]
        .drop("target_return")
    )

    correlation = correlation.sort_values(
        key=abs,
        ascending=False
    )

    print("\nFeature Correlation with Target Return")
    print("--------------------------------------")
    print(correlation.to_string())

    print("\nTop 5 correlated features:")
    print(correlation.head(5).to_string())


if __name__ == "__main__":
    analyze_feature_correlation()
